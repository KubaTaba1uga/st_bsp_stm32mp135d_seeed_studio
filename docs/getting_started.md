Getting Started
=====================

Using BSP starts from getting it's code:
```bash
git clone https://github.com/KubaTaba1uga/st_bsp_stm32mp135d_seeed_studio
cd st_bsp_stm32mp135d_seeed_studio
```

Now install dependencies required to perform the build:
```bash
sudo apt install python3-invoke
inv install
```

Once dependencies are in place, you are ready to run the build command:
```bash
inv build-bsp
```

If command completes succesfully, sdcard image will be under `build/buildroot/images/sdcard.img` path.

Now is the time to inject SD card into the PC and flash it:
```bash
sudo dd if=build/buildroot/images/sdcard.img of=/dev/sda bs=1M status=progress
```

Once flashing completes put the SD card into the board and await following messages coming over UART:
```txt
NOTICE:  CPU: STM32MP135D Rev.Y
NOTICE:  Model: Linux BSP for Seeed Studio STM32MP135D
NOTICE:  BL2: v2.10-stm32mp1-r2.0(release):v2.10-stm32mp-r2()
NOTICE:  BL2: Built : 14:25:22, May  1 2026
NOTICE:  BL2: Booting BL32
```

Debug config
--------------

The default configuration is great for daily usage, but if you need to do some development, debug image is much more better suited for the job. Debug image is not striped down from debug symbols and is build with all optimizations disabled, which simplifies usage of debugger or translating error traces. So if you need a debug config check out `inv build-bsp -c stm32mp135d_odyssey_debug_defconfig` command.
