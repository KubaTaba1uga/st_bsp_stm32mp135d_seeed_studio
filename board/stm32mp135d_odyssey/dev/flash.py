import subprocess
import time
import sys


def main():
    images = ["build/tf-a-stm32mp135d-odyssey-mx.stm32", "build/fip.bin", "build/boot.ext2"]
    for image in images:
        wait_for_dfu()
        cmd = f"dfu-util -a 0 -R -D {image}"
        print(cmd)
        dfu_util = subprocess.Popen(cmd, stdout=sys.stdout, shell=True)
        dfu_util.wait()
        if dfu_util.returncode != 251:
            print(f"DFU error! Exiting...")
            exit(1)
        time.sleep(0.1)

def wait_for_dfu():
    dfu_marker = "STMicroelectronics STM Device in DFU Mode"
    waits = 0
    while(True):
        with subprocess.Popen("lsusb", stdout=subprocess.PIPE) as lsusb:
            out = lsusb.stdout.read().decode()

        if dfu_marker in out:
            break;

        time.sleep(0.5)
        waits += 1

        if waits % 10 == 0:
            print("Waiting for dfu device")

if __name__ == "__main__":
    main()


