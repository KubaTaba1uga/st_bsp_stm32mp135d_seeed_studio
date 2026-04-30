## Seeed studio STM32MP135D BSP

To build bsp do:
```bash
❯ inv build-bsp
```

The image is build in `build/buildroot/images/sdcard.img`, to flash it onto sdcard being detected as `/dev/sda` do:
```bash
❯ sudo dd bs=4M conv=fsync if=build/buildroot/images/sdcard.img of=/dev/sda status=progress
```

### Supported peripherals

Currently supported peripherals are:
 - UART
 - SD card
 - USB
 - SWD
 - GPIO
 
Currently not supported peripherals are:
 - eMMC
 - Ethernet

 


