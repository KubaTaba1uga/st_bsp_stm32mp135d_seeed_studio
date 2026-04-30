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

Bootchain detects changes in the boot configuration and acts accordingly without any need to update the software. For more info about how we do it look into `STM32MP_USB_PROGRAMMER` config variable in TF-a, and also `bootcmd` variable in `board/stm32mp135d/uboot.env` file.

To speed up DFU transfer we have seperate boot partition. Inside the boot partition is only linux and linux device tree file so try keep it that way, bigger boot partition means more waiting during each DFU download.

Rom code and TF-A download firmware over USB and put it directly to RAM, linux however is booted diferently. U-boot download linux over USB and flash it to boot partition on SD card. Once linux and linux's device tree are on the SD card, uboot uses the card to perform the boot.

```{warning}
In case you need tf-a/optee/u-boot to be saved on the SD card remember to eject a card and flash it with `dd`.
```

```{warning}
DFU is only enabled in debug builds.
```

OpenOCD and GDB
------------------

Using OpenOCD require st-link v2 debugger like this [one](https://www.st.com/en/development-tools/st-link-v2.html). 

Watch out for clones cause every i tried didn't have working reset pin. I'm using reset all the time so decided to buy official ST version.

Once you manage to buy the hardware and connect it to the board according to the table:

```{csv-table} St-link v2 connection
:header: >
:    "St-link", "Board"
:widths: 20, 10

"PWR", Gpio pin 1
"GND", Gpio pin 6
"SWD IO", TP34
"SWD CLK", TP35
"SWD RST", TP36
```

If you are not familiar wit TPx syntax, check out [this section](hardware.md#swd).

After connecting the st-link with the board, connect st-link to your PC and run `inv openocde` from the bsp's root directory.

Now on another terminal start gdb with `inv gdb -p tf-a`. To connect to other parts of the boot chain you can change `-p tf-a` to `-p optee-os`, `-p u-boot` or `-p linux`.

```{note}
One of the features i'm using very often is openocd reboot, try it with `inv openocd -c reboot`. This way you can reset the board, so if anything went south you do not need to unplug power cord to the board again to reboot it!
```

