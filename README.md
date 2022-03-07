# OPTIGA™ TPM 2.0 Explorer
The OPTIGA™ TPM 2.0 Explorer is a GUI-based tool for users to familiarize themselves with TPM 2.0 quickly and easily using Infineon OPTIGA™ TPM 2.0 solution for Raspberry Pi. In addition, the OPTIGA™ TPM 2.0 Explorer demonstrates how the OPTIGA™ TPM 2.0 can be used to increase security and trust for data sharing, platform and cloud. 

Using this tool, you can start experiencing the benefits that the [OPTIGA™ TPM 2.0](https://www.infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-tpm/?redirId=39899/) will bring to smart home devices and network equipment.

| ![](/images/Setup/MainScreen.png) |
| ------------------------------------------------------- |

The main benefit from the tool is that you are able to explore OPTIGA™ TPM 2.0 features and learn use cases faster without having to be familiar with the TPM 2.0 as well as sets of commands. You simply select a button to call the relevant function or task. There is also an immediate visual feedback at the view menu for you to know what are the  commands run and corresponding responses after the button was selected. The ease of use of GUI has made it possible for all users in general, regardless of experience or knowledge, to access all kinds of OPTIGA™ TPM 2.0 features and use cases for commonly use. 

| ![](/images/Optiga_Setup/PCR/TPMPCRSHA1_ListAll.png) |
| ---------------------------------------------------- |

## Features

-   Allow for reading OPTIGA™ TPM 2.0 commands executed and the corresponded responses from the display screen or the terminal in the background
-   Display all properties defined within a OPTIGA™ TPM 2.0
-   Initialize a OPTIGA™ TPM 2.0
-   Reset back to default settings
-   Manage the authorization values for the owner, endorsement and lockout
-   Manage OPTIGA™ TPM 2.0 NV memory for creation, deletion, reading, writing, listing and etc
-   Handle PCR Indexes by listing all the different registers in SHA-1 or SHA-256
-   Handle PCR Indexes by extending a value into the registers in SHA-1 or SHA-256 using PCR Extend/Event
-   Manage specific handle and context associated with transient and persistent objects
-   Configure dictionary attack settings such as the number of attempts before lockout, the time taken for recovery from failure and lockout recovery
-   Create RSA-2048 and ECC-P256 primary and secondary key under storage hierarchy without supporting endorsement and platform hierarchy
-   Encrypt and decrypt data using RSA-2048
-   Sign and verify data with RSA-2048 and ECC-P256

## Use cases

-   Data Sealing with Policy
-   Remote attestation
-   Cryptographic operations using OpenSSL library
-   Secured communication with OpenSSL library
-   Device certificate provisioning and onboarding to AWS IoT core


## Hardware requirements

-   Raspberry Pi® 3 Model B+/ Raspberry Pi® 4 Model B
-   Micro SD card (≥8GB)
-   OPTIGA™ TPM 2.0 evaluation board
    -   [Iridium SLB 9670 TPM2.0](https://www.infineon.com/cms/en/product/evaluation-boards/iridium9670-tpm2.0-linux/) / [SLB 9672 TPM2.0](https://www.infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-tpm/optiga-tpm-slb-9672/) 
    

| ![](/images/Overview/TPMRPI3.png) |
| --------------------------------- |

## Setup Environment

This tool was tested on a Raspberry Pi® 3 Model B+/ 4 Model B with Raspbian Linux in Release Version 11 (Bullseye) and kernel version 5.10.92 with an Infineon OPTIGA™ TPM SLB 9670/ 9672 TPM2.0 evaluation board attached to the Raspberry Pi® board.

The following software required for the OPTIGA™ TPM 2.0 Explorer:
- python-wxtools
- tpm2-tss
- tpm2-tools
- tpm2-abrmd
- tpm2-tss-engine

For more information on how to setup the environment for the tool, you can refer to the [OPTIGA™ TPM 2.0 Explorer Setup Guide](./Setup%20Guide.md)

![](/images/Overview/RpiBullseye.png) 

## User Guide

Learn more about the tool, how it works and the functionalities of the OPTIGA™ TPM 2.0 by following graphical examples and simple step by step instructions - see the [OPTIGA™ TPM 2.0 Explorer User Guide](./User%20Guide.md) for details.

## Resources

You will find relevant resouces (tools, Open Source Host Code and Application notes) which can help you to study and learn OPTIGA™ TPM2.0 on [Infineon OPTIGA™ TPM2.0 Github Repo.](https://github.com/Infineon/optiga-tpm)

## License

The OPTIGA™ TPM 2.0 Explorer is released under the MIT License - see the [LICENSE](LICENSE) file for details.
