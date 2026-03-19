import os
import glob

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
              git libncurses5-dev python3"
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
    
