import os
import tempfile

from invoke import task

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BUILD_PATH = os.path.join(ROOT_PATH, "build")
DOCS_PATH = os.path.join(ROOT_PATH, "docs")

os.chdir(ROOT_PATH)
os.environ["PATH"] = f"{os.path.join(ROOT_PATH, '.venv', 'bin')}:{os.environ['PATH']}"


@task
def install(c):
    _pr_info(f"Installing dependencies...")

    try:
        c.run(
            "sudo apt-get install -y doxygen virtualenv \
              which sed make binutils build-essential diffutils \
              gcc g++ bash patch gzip bzip2 perl tar cpio \
              unzip rsync file bc findutils gawk curl \
              git libncurses5-dev python3 wget xxd"
        )

        c.run("virtualenv .venv")
        c.run(
            "pip install invoke myst-parser==5.0.0 sphinx==8.2.3 breathe==4.36.0 sphinx_rtd_theme==3.0.2 sphinx-autobuild==2025.08.25"
        )

    except Exception:
        _pr_error("Installing failed")
        raise

    _pr_info(f"Installing dependencies completed")


@task
def build_bsp(c, config="stm32mp135d_odyssey_prod_defconfig"):
    """
    @todo get urls and versions from config file
    """
    repos = {
        "buildroot": {
            "tag": "st/2024.02.9",
            "url": "https://github.com/bootlin/buildroot.git",
        },
        "linux": {
            "tag": "v6.6-stm32mp-r2",
            "url": "https://github.com/STMicroelectronics/linux.git",
        },
        "u-boot": {
            "tag": "v2023.10-stm32mp-r2",
            "url": "https://github.com/STMicroelectronics/u-boot.git",
        },
        "optee-os": {
            "tag": "4.0.0-stm32mp-r2",
            "url": "https://github.com/STMicroelectronics/optee_os.git",
        },
        "tf-a": {
            "tag": "v2.10-stm32mp-r2",
            "url": "https://github.com/STMicroelectronics/arm-trusted-firmware.git",
        },
    }
    _pr_info(f"Building BSP...")

    if "debug" in config:
        to_download = repos.items()
    else:
        to_download = [(repo, data) for (repo, data) in repos.items() if repo == "buildroot"]

    
    c.run("mkdir -p third_party")
    with c.cd("third_party"):
        for repo, rdata in to_download:
            if os.path.exists(os.path.join(ROOT_PATH, "third_party", repo)):
                continue
            c.run(f"git clone {rdata['url']} {repo}")
            with c.cd(repo):
                c.run(f"git checkout {rdata['tag']}")
                patches_dir = f"{ROOT_PATH}/board/stm32mp135d_odyssey/patches/{repo}"
                if os.path.exists(patches_dir):
                    c.run(f"find {patches_dir} -type f -exec git apply {{}} \\;")

    if config:
        configure(c, config)

    with c.cd("build/buildroot"):
        c.run("make")

    if "debug" in config:        
        with c.cd("build/buildroot/build/linux-custom"):
            c.run(
                "python scripts/clang-tools/gen_compile_commands.py && cp compile_commands.json ../../../../third_party/linux"
            )

        
    _pr_info(f"Building BSP completed")


@task
def configure(c, config="stm32mp135d_odyssey_prod_defconfig"):
    """
    Available configurations:
       - stm32mp135d_odyssey_prod_defconfig
       - stm32mp135d_odyssey_debug_defconfig
    """
    _pr_info(f"Configuring buildroot...")

    with c.cd("third_party/buildroot"):
        flags = [
            "O=../../build/buildroot",
            "BR2_EXTERNAL=../../.",
            config,
        ]

        c.run(f"make " + " ".join(flags))

    _pr_info(f"Configuring buildroot completed")


@task
def docs_build(c):
    _pr_info("Building docs...")

    docs_path = os.path.join(BUILD_PATH, "docs", "html")

    c.run("mkdir -p %s" % BUILD_PATH)
    try:
        c.run("doxygen docs/Doxyfile")
        with c.cd(DOCS_PATH):
            c.run(f"sphinx-build -b html . {docs_path}")
    except Exception:
        _pr_error(f"Building docs failed")
        raise

    _pr_info("Building docs completed")


@task
def docs_serve(c, port=8000):
    _pr_info("Serving docs...")

    docs_build(c)

    c.run(
        " ".join(
            [
                f"sphinx-autobuild",
                f"--port {port}",
                f"docs build/docs/html",
            ]
        ),
        pty=True,
    )

    _pr_info("Serving docs completed")


@task
def deploy_sdcard(c, dev="sda"):
    _pr_info(f"Deploying to sdcard...")

    if not os.path.exists("/dev/disk/by-partlabel/fsbl1"):
        raise ValueError("No /dev/disk/by-partlabel/fsbl1")
    if not os.path.exists("/dev/disk/by-partlabel/fsbl2"):
        raise ValueError("No /dev/disk/by-partlabel/fsbl2")
    if not os.path.exists("/dev/disk/by-partlabel/fip"):
        raise ValueError("No /dev/disk/by-partlabel/fip")

    with c.cd("build/buildroot/images"):
        c.run(
            "sudo dd if=tf-a-stm32mp135d-odyssey_dev_minimal_dt-mx.stm32 of=/dev/disk/by-partlabel/fsbl1 bs=1K conv=fsync"
        )
        c.run(
            "sudo dd if=tf-a-stm32mp135d-odyssey_dev_minimal_dt-mx.stm32 of=/dev/disk/by-partlabel/fsbl2 bs=1K conv=fsync"
        )
        c.run("sudo dd if=fip.bin of=/dev/disk/by-partlabel/fip bs=1K conv=fsync")

    c.run("sudo sync")

    _pr_info(f"Deploy to sdcard completed")

@task
def gdb(c, phase="tf-a", runetime_attach=False):
    """
    Phase selects which firmware will be used for debugging.
    Available `phase` values are:
       - tf-a
       - optee-os
       - u-boot
       - linux

    Runetime attach decides whether to force reset before
    attaching debugger or attach it to CPU as it is.
    Setting `runetime_attach` to True means we won't do reset.
    """
    stage_phase_map = {
        "tf-a": 1,
        "optee-os": 2,
        "u-boot": 3,
        "linux": 4,
    }
    _pr_info(f"Running gdb...")
    debug_phase = stage_phase_map.get(phase)
    if not debug_phase:
        raise ValueError(f"Wrong {phase=}")

    debug_mode = 0
    if runetime_attach:
        debug_mode = 1

    tools_path = os.path.join(ROOT_PATH, "tools", "gdb")        
    with open(os.path.join(tools_path, "init.gdb"), "r") as src:
        src_txt = src.read()
        
    src_txt = src_txt.replace("set $debug_phase = 1", f"set $debug_phase = {debug_phase}", count=1)
    src_txt = src_txt.replace("set $debug_mode = 0", f"set $debug_mode = {debug_mode}", count=1)            

    with tempfile.NamedTemporaryFile(
            "w", prefix="init", suffix=".gdb", delete_on_close=False
    ) as dst:
        dst.write(src_txt)
        dst.close()  
                
        with c.cd(tools_path):
            c.run(f"gdb-multiarch -x {str(dst.name)}", pty=True)


@task
def openocd(c, command: str | None = None):
    all_commands = {
        'reboot': ["init", "reset run", "shutdown"]
    }
    
    cmd = "openocd -f board/stm32mp13x_dk.cfg"
    commands = []
    
    if command:
        commands = all_commands.get(command)

    if commands:
        cmd += " " + " ".join(f"-c '{command}'" for command in commands)
        
    c.run(cmd, pty=True)
    
    
    
    
###############################################
#                Private API                  #
###############################################
def _pr_info(message: str):
    print(f"\033[94m[INFO] {message}\033[0m")


def _pr_warn(message: str):
    print(f"\033[93m[WARN] {message}\033[0m")


def _pr_debug(message: str):
    print(f"\033[96m[DEBUG] {message}\033[0m")


def _pr_error(message: str):
    print(f"\033[91m[ERROR] {message}\033[0m")

