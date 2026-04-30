################################################################################
#
# stm32wrapper4dbg
#
################################################################################

STM32WRAPPER4DBG_VERSION = v5.1.2
STM32WRAPPER4DBG_SITE = $(call github,STMicroelectronics,stm32wrapper4dbg,$(STM32WRAPPER4DBG_VERSION))

define STM32WRAPPER4DBG_BUILD_CMDS
	cd "$(@D)" ; \
	PATH=$(BR_PATH) $(MAKE)
endef

define STM32WRAPPER4DBG_INSTALL_TARGET_CMDS
	cd "$(@D)" ; \
	$(INSTALL) -m 0755 stm32wrapper4dbg $(HOST_DIR)/bin/
endef

$(eval $(generic-package))
