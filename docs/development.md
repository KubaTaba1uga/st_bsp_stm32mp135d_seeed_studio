Development
===============

During development you find some tricks and hacks that make stuff quicker, in this section we aim to gather them all together.

DFU
----

Device firmware update (DFU) protocol allow downloading firmware to the device via USB. 

We use DFU to update the firmware on the SD card without ejecting it from the board.

To use DFU we need first to adjust boot pins, to make 101 postion. You should put jumpers between first and third pair of boot pins. Then use usb C cable to connect PC to the Seeed Studio board, and run dfu flashing script (before running the script remember to build the bsp):
```bash
python boards/stm32mp135d_odyssey/debug/flash.py
```

Bootchain detects changes in the boot configuration and acts accordingly without any need to update the software. For more info about how we do it look into `STM32MP_USB_PROGRAMMER` config variable in TF-a, and also bootcmd variable in `board/stm32mp135d/uboot.env` file.
