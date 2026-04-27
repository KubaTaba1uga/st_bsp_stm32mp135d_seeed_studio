#!/bin/bash

# copy uboot init script into the target image
mkdir ${BINARIES_DIR}/boot

cp "${BINARIES_DIR}/boot.scr" \
   "${TARGET_DIR}/boot/boot.scr"
