# **OPTIGA™ TPM 2.0 Explorer Setup Guide**

This page provides instructions on how to install and configure the Raspberry Pi to enable the [OPTIGA™ TPM 2.0](https://www.infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-tpm/?redirId=39899/) in order to use the OPTIGA™ TPM 2.0 Explorer.

1.  [Prerequisites](#prerequisites)
2.  [Enable OPTIGA™ TPM 2.0 support on Raspberry Pi](#enabletpm)
3.  [Set up VNC Connection](#vnc-connection-setup-optional)
4.  [Install OPTIGA™ TPM 2.0 Explorer](#install-tpm_explorer)
5.  [References](#references)

## Prerequisites 

-   Raspberry Pi 3 Model B+ / Raspberry Pi 4 Model B
-   Micro SD card (≥8GB) flashed with Raspberry Pi Bullseye OS (Released on 2022-01-28). Download the official image from [[1]](#references).
-   OPTIGA™ TPM 2.0 evaluation board
    -   [Iridium SLB 9670 TPM2.0](https://www.infineon.com/cms/en/product/evaluation-boards/iridium9670-tpm2.0-linux/)

| ![](/images/Overview/TPMRPI3.png) |
| --------------------------------- |



**Table 1** shows a summary of the hardware and environment used.

| Hardware             | Version   and Firmware/OS                                    | Comment                                                      |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Host  PC             | • x86  architecture and USB 2.0 (or higher)  •  Capable of running Linux, for example Ubuntu 18.04  •  Arbitrary as long as VNC viewer is present | This  platform is used for patching the Kernel, maintaining and interacting with  the Raspberry Pi in a more convenient and faster way compared to doing all  actions directly on the Raspberry Pi. |
|  OPTIGA™ TPM 2.0 evaluation board       |  • [Iridium SLB 9670 TPM2.0](https://www.infineon.com/cms/en/product/evaluation-boards/iridium9670-tpm2.0-linux/) | This  board contains the Infineon OPTIGA™ TPM SLB 9670 TPM2.0 mounted on an  easy-to-use hardware board, which can be attached to the Raspberry Pi. |
| Raspberry  Pi Board | •  Model 3 B+/ 4 B, Bullseye OS (2022-01-28)   •  Micro SD Card with at least 8 GB   •  Micro-B/ Type C USB cable for power supply | A SD  card with Raspberry Pi Bullseye OS and kernel version 5.10.92 on it is required, which can be downloaded at [[1]](#references). This SD card will be  plugged in the developer PC |



**Table 2** shows a summary of the software used.

| Software        | Version    | Comment                                                      |
| --------------- | ---------- | ------------------------------------------------------------ |
| tpm2-tools      | 5.2        | https://github.com/tpm2-software/tpm2-tools Tag: ebd59ef827f1fc8e0efa43f9cade4d3d7efee59a |
| tpm2-abrmd      | 2.4.1      | https://github.com/tpm2-software/tpm2-abrmd Tag: 71bfb9457267683e1f6a6dea42622442a62203a5 |
| tpm2-tss        | 3.2.0      | https://github.com/tpm2-software/tpm2-tss Tag: e237e4d33cbf280292a480edd8ad061dcd3a37a2 |
| tpm2-tss-engine | 1.1.0      | https://github.com/tpm2-software/tpm2-tss-engine Tag: 6f387a4efe2049f1b4833e8f621c77231bc1eef4 |



## <a name="enabletpm"></a>Enable OPTIGA™ TPM 2.0 support on Raspberry Pi

Insert the flashed SD card and boot the Raspberry Pi.

Open the configuration file in an editor:  

```shell
sudo nano /boot/config.txt   
```

Insert the following lines to enable SPI and TPM: 

```shell
dtoverlay=tpm-slb9670
```

Save the file and exit the editor.  



## <a name="vnc-connection-setup-optional"></a>Set up VNC Connection

This optional step will guide you on how to set up a VNC connection from your RPI to your computer. This step requires a flashed MicroSD with the OPTIGA™ TPM Explorer image in an RPI3 and VNC Viewer installed on your computer.

Start-up the Raspberry Pi with HDMI cable to monitor and start the terminal.

| ![](/images/Setup/terminal.png) |
| ------------------------------- |

**Figure 1**: RPI Home Screen on monitor

 Enter the Raspberry Pi Software Configuration Menu

```shell
sudo raspi-config
```

Select option 5 Interfacing Options.

| ![](/images/Setup/raspi-config.png) |
| --------------------------------------------------------- |

**Figure 2**: Raspberry Pi Software Configuration Tool

Select P2 SSH and enable.

| ![](/images/Setup/ssh.png) |
| ------------------------------------------------ |

**Figure 3**: SSH Selection

| ![](/images/Setup/ssh_enable.png) |
| ------------------------------------------------------- |

**Figure 4**: SSH Enable

Select P3 VNC and enable.

| ![](/images/Setup/vnc.png) |
| ------------------------------------------------ |

**Figure 5**: VNC Selection

| ![](/images/Setup/vnc_enable.png) |
| ------------------------------------------------------- |

**Figure 6**: VNC Enable

Select  SPI and enable.

| ![](/images/Setup/spi.png) |
| -------------------------- |

**Figure 7**: SPI Selection

| ![](/images/Setup/spi_enable.png) |
| --------------------------------- |

**Figure 8**: SPI Enable

Select finish and return to the terminal

| ![](/images/Setup/terminal2.png) |
| ------------------------------------------------------ |

**Figure 9**: Raspberry Pi Terminal

Enter "hostname -I" into the terminal and copy the IP address

```shell
hostname -I       
192.168.###.###
```

Paste the IP Address of RPI3 into VNC Viewer and connect.

| ![](/images/Setup/VNCViewer.png) |
| ------------------------------------------------------ |

**Figure 10**: VNC Viewer Connection Screen

Enter the Username and the Password.

Username: pi

Password:  Enter your RPI password

| ![](/images/Setup/VNCViewerUserPass.png) |
| ------------------------------------------------------------ |

**Figure 11**: VNC Viewer Authentication Menu

You should be successfully connected and able to view the RPI through VNC connection on your device.

| ![](/images/Setup/RPIHomeScreen_VNC.png) |
| ------------------------------------------------------------ |

**Figure 12**: RPI Home Screen on VNC Viewer



## <a name="install-tpm_explorer"></a> Install OPTIGA™ TPM 2.0 Explorer 

Download TPM Explorer Source Code (Approx. 175MB):  
via: https://github.com/Infineon/optiga-tpm-explorer/releases
or 

via https:
```shell
git clone https://github.com/Infineon/optiga-tpm-explorer.git
```
via ssh:(Need to setup SSH keys associated with your account)
```shell
git clone git@github.com:Infineon/optiga-tpm-explorer.git
```
Execute Installation script:
```shell
cd optiga-tpm-explorer
./installation_script.sh
```



The installation script installs the following dependencies required and compiles the source code for the OPTIGA™ TPM 2.0 Explorer Application.
-   python-wxtools
-   tpm2-tss
-   tpm2-tools
-   tpm2-abrmd
-   tpm2-tss-engine

Once complete, to run from source:

```shell
cd ~/optiga-tpm-explorer/Python_TPM20_GUI
python main.py
```
To run from binary:

go to your home directory and access the file called TPM_Explorer.

| ![](/images/Settingup_TPMExplorer/TPM_Explorer.png) |
| ------------------------------------------------------------ |

**Figure 13**: TPM_Explorer File Directory

Next, access the file called Python_TPM20_GUI.

| ![](/images/Settingup_TPMExplorer/Python_TPM20_GUI.png) |
| ------------------------------------------------------------ |

**Figure 14**: Python_TPM20_GUI File Directory

Next, enter the bin file.

| ![](/images/Settingup_TPMExplorer/binfile.png) |
| ------------------------------------------------------------ |

**Figure 15**: Python_TPM20_GUI Bin File Directory

Execute "start_gui.sh" and select execute in terminal.

| ![](/images/Settingup_TPMExplorer/start_gui.png) |
| ------------------------------------------------------------ |

**Figure 16**: Selecting start_gui.sh

| ![](/images/Settingup_TPMExplorer/execute.png) |
| ------------------------------------------------------------ |

**Figure 17**: Executing start_gui.sh in terminal

A terminal will pop up and the OPTIGA TPM 2.0 Explorer interface will be open.

| ![](/images/Setup/MainScreen.png) |
| ------------------------------------------------------- |

**Figure 18**: Home Screen of OPTIGA TPM 2.0 Explorer

For more information on the OPTIGA™ TPM 2.0 Explorer, please refer to the [OPTIGA™ TPM 2.0 Explorer User Guide](./User%20Guide.md).

## References

1.  <https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2022-01-28/>
