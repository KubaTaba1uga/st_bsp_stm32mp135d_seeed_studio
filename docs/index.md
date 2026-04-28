BSP for STM32MP135D from Seeed Studio
====================================================

This is BSP for STM32MP135D from Seeed Studio. To build the BSP we use buildroot.

Someone may ask, why create another buildroot BSP when there is already one [here](https://github.com/xogium/buildroot-stm32mp135d-odyssey)?

The BSP created by Xogium uses linux/uboot/optee/tf-a repos maintained by Xogium which makes upgrading more difficult cause you can't
see straigthaway what changes were done from mainline. Additionally all device tree files are embedded into the repositories which make
modifying them harder cause you need to go into the repo find appropriate device tree and then copy it into buildroot etc. 

We aim to centralize all code which differ from mainline ST repos into this buildroot repository, which should make things easier like upgrading 
some stack component or seeing changes made to support the board. 

Our end goal is having one tag per Linux version we support. Other bootchain components versions will be adjusted to linux.

All changes required to support the board are mantained via patches.

---

This documentation is splitted into lously connected sections. The documentation contains topics which i needed to understand better to create the BSP,
so if you find something missing, feel free to contribute. Anyhow, here are the sections:

```{toctree}
:maxdepth: 2

hardware
development
```



