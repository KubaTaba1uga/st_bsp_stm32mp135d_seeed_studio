if test $boot_device = "mmc" && test $boot_instance = "0"; then
	echo "Micro sd card boot" &&
	ext4load mmc 0:5 0xC2400000 /boot/stm32mp135d-odyssey_dev_minimal_dt-mx.dtb &&
	ext4load mmc 0:5 0xC0200000 /boot/zImage &&
	setenv bootargs "root=/dev/mmcblk0p5 rootwait rw quiet console=ttySTM0,115200n8 earlycon";
fi

if test $boot_device = "mmc" && test $boot_instance = "1"; then
	echo "eMMC boot" &&
	ext4load mmc 1:2 0xC2400000 /boot/stm32mp135d-odyssey_dev_minimal_dt-mx.dtb &&
	ext4load mmc 1:2 0xC0200000 /boot/zImage &&
	setenv bootargs "root=/dev/mmcblk1p2 rootwait rw quiet console=ttySTM0,115200n8 earlycon";
fi

bootz 0xC0200000 - 0xC2400000
