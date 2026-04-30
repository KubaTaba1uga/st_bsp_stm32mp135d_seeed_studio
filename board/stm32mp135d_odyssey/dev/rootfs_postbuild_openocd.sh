#!/bin/sh

set -xeu

sh $BR2_EXTERNAL_SEEED_STUDIO_PATH/board/stm32mp135d_odyssey/dev/rootfs_postbuild.sh

stm32wrapper4dbg -s ${BINARIES_DIR}/tf-a-stm32mp135d-odyssey-mx.stm32 -d ${BINARIES_DIR}/tf-a-stm32mp135d-odyssey-mx-debug.stm32 -b -f

cp ${BINARIES_DIR}/tf-a-stm32mp135d-odyssey-mx-debug.stm32 ${BINARIES_DIR}/tf-a-stm32mp135d-odyssey-mx.stm32

echo ${BINARIES_DIR}
