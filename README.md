## Seeed studio STM32MP135D BSP

To build bsp do:
```bash
❯ inv build-bsp
```

The image is build in `build/buildroot/images/sdcard.img`, to flash it onto sdcard being detected as `/dev/sda` do:
```bash
❯ sudo dd bs=4M conv=fsync if=build/buildroot/images/sdcard.img of=/dev/sda status=progress
```

More info about the BSP can be found in docs [here](https://kubataba1uga.github.io/st_bsp_stm32mp135d_seeed_studio/index.html).

### Supported peripherals

Currently we support following peripherals:
 - HSE Clock
 - DDR RAM
 - PMIC
 - BSEC
 - UART
 - SDMMC
 - ETZPC
 - USB-A
 - USB-C (OTG)
 - SWD
 
Currently not supported peripherals are:
 - eMMC
 - Ethernet

 


