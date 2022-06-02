# **OPTIGA™ TPM 2.0 Explorer User Guide**


This page helps you explore the tool to accelerate your learning about OPTIGA™ TPM 2.0. 

1. [Overview](#overview)
    - [1.1 Features](#features)
    - [1.2 Use cases](#use-cases)
    - [1.3 Setup environment](#setup-environment)
2.  [Setup and Basic Features](#setup-and-basic-features)
    - [2.1 Setup](#setup)
        - [2.1.1 OPTIGA™ TPM Setup Functions](#optiga-tpm-setup-functions)
        - [2.1.2 TPM Startup](#tpm-startup)
        - [2.1.3 Viewing TPM (fixed) Capabilities](#viewing-tpm-fixed-capabilities)
        - [2.1.4 Changing Authorization values of TPM](#changing-authorization-values-of-tpm)
        - [2.1.5 Dictionary Attack](#dictionary-attack)
        - [2.1.6 TPM ClearLock](#tpm-clearlock)
    - [2.2 Platform Configuration Registers](#platform-configuration-registers)
        - [2.2.1 Platform Configuration Registers Functions](#platform-configuration-registers-functions)
        - [2.2.2 PCR Listing](#pcr-listing)
        - [2.2.3 PCR Extend and PCR Event](#pcr-extend-and-pcr-event)
    - [2.3 NVM and Certificate Management](#nvm-and-certificate-management)
        - [2.3.1 NVM and Certificate Management Functions](#nvm-and-certificate-management-functions)
        - [2.3.2 NV Define](#nv-define)
        - [2.3.3 NV Write](#nv-write)
        - [2.3.4 Reading Cerificiate](#reading-cerificiate)
        - [2.3.5 Writing File](#writing-file)
        - [2.3.6 NV Release](#nv-release)
    - [2.4 Handle Mangement](#handle-mangement)
        - [2.4.1 Handle Management Functions](#handle-management-functions)
        - [2.4.2 Handle Management List All](#handle-management-list-all)
        - [2.4.3 Handle Management Evict Persistent](#handle-management-evict-persistent)
3.  [Cryptographic Functions](#cryptographic-functions)
    - [3.1 Hash Cryptographic Functions](#hash-cryptographic-functions)
    - [3.2 RSA Cryptographic Functions](#rsa-cryptographic-functions)
        - [3.2.1 RSA Cryptographic Function Description](#rsa-cryptographic-function-description)
        - [3.2.2 Creating RSA Keypair](#creating-rsa-keypair)
        - [3.2.3 Encrypting and Decrypting RSA](#encrypting-and-decrypting-rsa)
        - [3.2.4 Signing and Verifying RSA](#signing-and-verifying-rsa)
     - [3.3 ECC Cryptographic Functions](#ecc-cryptographic-functions)
        - [3.3.1 ECC Cryptographic Function Description](#ecc-cryptographic-function-description)
        - [3.3.2 Creating ECC Keypair](#creating-ecc-keypair)
        - [3.3.3 Signing and Verifying ECC](#signing-and-verifying-ecc)
4.  [OpenSSL Engine](#openssl-engine)
    - [4.1 RSA (Enc/Dec/Sign/Verify)](#rsa-encdecsignverify)
        - [4.1.1 RSA (Enc/Dec/Sign/Verify) Function Description](#rsa-encdecsignverify-function-description)
        - [4.1.1.1 RSA Encryption and Decryption](#rsa-encryption-and-decryption)
        - [4.1.1.2 RSA Signing and Verification](#rsa-signing-and-verification)
    - [4.2 Random Number Generator](#random-number-generator)
    - [4.3 RSA (Client/Server)](#rsa-clientserver)
        - [4.3.1 RSA (Client/Server) Function Description](#rsa-clientserver-function-description)
        - [4.3.2 Create Root CA and Its Certificate](#create-root-ca-and-its-certificate)
        - [4.3.3 Create Server Certificate](#create-server-certificate)
        - [4.3.4 Create an OpenSSL Server](#create-an-openssl-server)
        - [4.3.5 Create an OpenSSL Client](#create-an-openssl-client)
        - [4.3.6 Secure data exchange between Server and Client](#secure-data-exchange-between-server-and-client)
    - [4.4 ECC (Client/Server)](#ecc-clientserver)
        - [4.4.1 ECC (Client/Server) Function Description](#ecc-clientserver-function-description)
        - [4.4.2 Create Root CA and Its Certificate](#create-root-ca-and-its-certificate-1)
        - [4.4.3 Create Server Certificate](#create-server-certificate-1)
        - [4.4.4 Create an OpenSSL Server](#create-an-openssl-server-1)
        - [4.4.5 Creating an OpenSSL Client](#creating-an-openssl-client)
        - [4.4.6 Secure data exchange between Server and client](#secure-data-exchange-between-server-and-client-1)
5.  [Data Sealing with Policy](#data-sealing-with-policy)
    - [5.1 Data Sealing with Policy Function Description](#data-sealing-with-policy-function-description)
    - [5.2 Data Sealing with Policy Functions](#data-sealing-with-policy-functions)
        - [5.2.1 Data Sealing with Policy](#data-sealing-with-policy-1)
6.  [Attestation](#attestation)
    - [6.1 Attestation Function Description](#attestation-function-description)
    - [6.2 Generating Quote](#generating-quote)
    - [6.3 Verifying Quote](#verifying-quote)
    - [6.4 Evict AK/EK Handle](#evict-akek-handle)
7.  [Secured connection to AWS IoT core using TPM2.0](#secured-connection-to-aws-iot-core-using-tpm2.0)
    - [7.1 Get started with AWS IoT Core](#get-started-with-aws-iot-core)
    - [7.2 Create device certificate and assign it to Thing with policy](#create-device-certificate-and-assign-it-to-thing-with-policy)
    - [7.3 Publish messages to AWS IoT core from the Raspberry Pi](#publish-messages-to-aws-iot-core-from-the-raspberry-pi)
8.  [References](#references)

# Overview

The OPTIGA™ TPM 2.0 Explorer is a GUI-based tool for users to familiarize themselves with TPM 2.0 quickly and easily using Infineon's OPTIGA™ TPM 2.0 solution for Raspberry Pi. In addition, the OPTIGA™ TPM 2.0 Explorer demonstrates how the OPTIGA™ TPM 2.0 can be used to increase security and trust for data sharing across different networking and cloud platforms.

Using this tool, you can instantly experience the benefits that [OPTIGA™ TPM 2.0](https://www.infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-tpm/?redirId=39899/) will bring to IoT devices and network equipment.

## Features

-   Shows OPTIGA™ TPM 2.0 commands executed and the corresponding responses on the display screen or the terminal in the background
-   Displays all properties defined within an OPTIGA™ TPM 2.0
-   Initializes an OPTIGA™ TPM 2.0
-   Resets back to default settings
-   Manages the authorization values for the owner, endorsement and lockout
-   Manages OPTIGA™ TPM 2.0 NV memory for creating, deleting, reading, writing, listing, etc.
-   Handles PCR indexes by listing all the different registers in SHA-1 or SHA-256
-   Handles PCR indexes by extending a value to the registers in SHA-1 or SHA-256 using PCR Extend/Event
-   Manages specific handles and contexts associated with transient and persistent objects
-   Configures dictionary attack settings such as the number of attempts before lockout as well as the time required for recovery from failure and from lockout
-   Creates RSA-2048 and ECC-P256 primary and secondary keys under storage hierarchy without supporting endorsement and platform hierarchy
-   Encrypts and decrypts data using RSA-2048
-   Signs and verifies data with RSA-2048 and ECC-P256

## Use cases

-   Data sealing with policy
-   Remote attestation
-   Cryptographic operations using OpenSSL library
-   Secured communications with OpenSSL library
-   Device certificate provisioning and onboarding to AWS IoT Core

## Setup environment

For more information on how to setup the tool environment, refer to the [OPTIGA™ TPM 2.0 Explorer Setup Guide](./Setup%20Guide.md)

This tool was tested on a Raspberry Pi (RPi) 3 Model B+/ RPi 4 Model B with Raspbian Linux in Release Version 11 (Bullseye) and kernel version 5.10.92 using an Infineon OPTIGA™ TPM SLB 9670 TPM2.0 attached to the Raspberry Pi board (Figure 1 and Figure 2).

![](/images/Overview/RpiBullseye.png) 

Figure 1: Raspbian Linux 11 (Bullseye) and kernel version 5.10.92

![](/images/Overview/TPMRPI3.png) 

Figure 2: Infineon Iridium SLB 9670 TPM2.0 SPI Board on a Raspberry Pi 3



**Table 1** shows a summary of the hardware and environment used.

| Hardware             | Version   and Firmware/OS                                    | Comment                                                      |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Host  PC             | • x86  architecture and USB 2.0 (or higher)  •  Capable of running Linux, for example Ubuntu 18.04  •  Arbitrary as long as VNC viewer is present | This  platform is used for patching the Kernel, maintaining and interacting with  the Raspberry Pi in a more convenient and faster way compared to doing all  actions directly on the Raspberry Pi. |
| OPTIGA™ TPM 2.0 evaluation board      | • [Iridium SLB 9670 TPM2.0](https://www.infineon.com/cms/en/product/evaluation-boards/iridium9670-tpm2.0-linux/) | This  board contains the Infineon OPTIGA™ TPM SLB 9670 TPM2.0 mounted on an  easy-to-use hardware board, which can be attached to the Raspberry Pi. |
| Raspberry  Pi Board | •  Model 3 B+/ 4 B, Bullseye OS (2022-01-28)   •  Micro SD Card with at least 8 GB   •  Micro-B/ Type C USB cable for power supply | A SD  card with Raspberry Pi Bullseye OS and kernel version 5.10.92 on it is required, which can be downloaded at [[1]](#references). This SD card will be  plugged in the developer PC |



**Table 2** shows a summary of the software used.

| Software        | Version    | Comment                                                      |
| --------------- | ---------- | ------------------------------------------------------------ |
| tpm2-tools      | 5.2        | https://github.com/tpm2-software/tpm2-tools Tag: ebd59ef827f1fc8e0efa43f9cade4d3d7efee59a |
| tpm2-abrmd      | 2.4.1      | https://github.com/tpm2-software/tpm2-abrmd Tag: 71bfb9457267683e1f6a6dea42622442a62203a5 |
| tpm2-tss        | 3.2.0      | https://github.com/tpm2-software/tpm2-tss Tag: e237e4d33cbf280292a480edd8ad061dcd3a37a2 |
| tpm2-tss-engine | 1.1.0      | https://github.com/tpm2-software/tpm2-tss-engine Tag: 6f387a4efe2049f1b4833e8f621c77231bc1eef4 |



# Setup and Basic Features

This section shows you the Setup features of the OPTIGA™ TPM 2.0 Explorer.

## Setup 

Select "Setup and Basic Features".

| ![](/images/Optiga_Setup/Setup/MainScreen.png) |
| ---------------------------------------------- |

Figure 3: Setup and Basic Features Selection

| ![](/images/Optiga_Setup/Setup/Setup_Unedited/TPM_SetupScreen.png) |
| ------------------------------------------------------------ |

Figure 4: OPTIGA™ TPM Setup Menu Screen



### OPTIGA™ TPM Setup Functions

Setup function descriptions 

| ![](/images/Optiga_Setup/Setup/TPM_SetupScreen1.png) |
| ---------------------------------------------------- |

Figure 5: OPTIGA™ TPM Setup Menu Function Descriptions


 ### <a name="tpm-startup"></a>TPM Startup

The OPTIGA™ TPM will startup by issuing the TPM2_startup command using TPM2 tools when the RPI is powered on. However, if the reset button is pressed, the TPM2_startup command must be invoked separately by clicking on the "Startup" button before running any TPM command or operation. Otherwise, the error message will be displayed "WARNING:esys:src/tss2-esys/api/Esys_StartAuthSession.c:390:Esys_StartAuthSession_Finish() Received TPM Error" if the "Startup" button is not selected prior to "Get TPM Capability (variable)" button.  

| ![](/images/Optiga_Setup/Setup/TPMResetStartupfail.png) |
| ------------------------------------------------------- |

Figure 6: Display TPM capability (variable) failure due to reset without running TPM2_startup

To startup the OPTIGA™ TPM, select the "Startup" button at (1). Then, check if the TPM is functional by selecting "Get TPM Capability (variable)" at (2). TPM variable parameters can now be displayed.  

| ![](/images/Optiga_Setup/Setup/TPMResetStartupSuccess.png) |
| ---------------------------------------------------------- |

Figure 7: Display TPM capability (variable) successfully after TPM2_startup



### Viewing TPM (fixed) Capabilities

The TPM capabilities (fixed) can be displayed using tpm2_getcap properties-fixed in TPM2 tools. The fixed capabilities shows important information such as the TPM vendor and the firmware version. It also displays the manufacturer as well as many other information.

To view fixed capabilities and details, select "Get TPM Capability (fixed)". 

| ![](/images/Optiga_Setup/Setup/TPM_GetFixed.png) |
| ------------------------------------------------ |

Figure 8: Setup Menu Select Get TPM capability (fixed)

Information such as the manufacturer, firmware and more can be found here.  

| ![](/images/Optiga_Setup/Setup//Setup_Unedited/SetAuthSuccessCheckTPMFixed.png) |
| ------------------------------------------------------------ |

Figure 9: Setup Menu display Get TPM capability (fixed)



### Changing Authorization values of TPM

First, perform a "TPM Clear" at (1) so that the TPM will be reconfigured to default mode. Then select "Get TPM capability (variable)" at (2) to display default TPM variable parameters. When the owner, endorsement and lockout authorization values are not changed, the variable value should be '0'.

**WARNING:** Performing a TPM Clear will result in the reset of the TPM.

| ![](/images/Optiga_Setup/Setup/PlatformClear2.png) |
| -------------------------------------------------- |

Figure 10: Display default TPM capability(variable) after reset back to default mode

To change the lockout, endorsement, and owner authorization values of TPM, select "Change Auth".  

| ![](/images/Optiga_Setup/Setup/TPM_ChangeAuth.png) |
| -------------------------------------------------- |

Figure 11: Take TPM ownership by configuring the authorization values for TPM to be used first time or after reset the TPM to default mode

Select "SET ALL" to confirm the credentials. In this example, we will use the default values already given. 

| ![](/images/Optiga_Setup/Setup/SetAuthScreen.png) |
| ------------------------------------------------- |

Figure 12: Configure authorization values

Once successful, select "Get TPM capability (variable)" to confirm the results. The first 3 AuthSet values should be 1 once the owner, endorsement and lockout authorization value values are set. 

| ![](/images/Optiga_Setup/Setup/SetAuthSuccessCheckTPMVari.png) |
| ------------------------------------------------------------ |

Figure 13: Display TPM capability (variable) to confirm if the authorization values are set



### Dictionary Attack

Select "Dictionary Attack Settings" to configure settings for dictionary attacks.

| ![](/images/Optiga_Setup/Setup/Dictionaryattacksel.png) |
| ------------------------------------------------------- |

Figure 14: Setup Menu Select Dictionary Attack Settings

Configure the dictionary attack settings and select "OK" to confirm. You can change the number of attempts before lockout, the time taken for recovery from failure and lockout recovery.

| ![](/images/Optiga_Setup/Setup/DictionaryAttackSettings.png) |
| ------------------------------------------------------------ |

Figure 15: Dictionary Attack Settings Configuration

Dictionary Attack Settings should be successfully configured.

| ![](/images/Optiga_Setup/Setup//Setup_Unedited/DictionaryAttackSettingsSuccess.png) |
| ------------------------------------------------------------ |

Figure 16: Dictionary Attack Settings Successfully Configured shown on TPM Capability (Variable)



### TPM ClearLock

The TPM ClearLock in TPM2 tools will effectively block/unblock lockout authorization handle for issuing TPM clear. This is to prevent TPM reset to default mode.

To disable 'tpm2_clear' command, select "Disable Clear ON" at (1). Then, select "Platform Clear" at (2). It should fail.

| ![](/images/Optiga_Setup/Setup/PlatformClearON.png) |
| --------------------------------------------------- |

Figure 17: TPM Clearlock Disable Clear On Succeeded

To re-enable "Platform Clear", select "Disable Clear OFF" at (1) to disable clearlock. Then, perform a "Platform Clear" at (2) and check variable using "Get TPM capability (variable)" at (3). AuthSet should be successfully cleared.

| ![](/images/Optiga_Setup/Setup/PlatformDisableClearOffSucess.png) |
| ------------------------------------------------------------ |

Figure 18: TPM Clearlock Disable Clear Off succeeded



## Platform Configuration Registers

This section shows you the functionalities of the PCR in the OPTIGA™ TPM.

From the "Setup and Basic Features" menu, select the "Platform Confiuguration Registers".

| ![](/images/Optiga_Setup/PCR/SelectPCR.png) |
| ------------------------------------------- |

Figure 19: Platform Configuration Registers Selection

| ![](/images/Optiga_Setup/PCR/PCR_Unedited/TPMPCRScreen.png) |
| ----------------------------------------------------------- |

Figure 20: Platform Configuration Registers Menu



### Platform Configuration Registers Functions

Platform Configuration Register function descriptions

| ![](/images/Optiga_Setup/PCR/TPMPCRScreen.png) |
| ---------------------------------------------- |

Figure 21: OPTIGA™ TPM Platform Configuration Registers Functions Descriptions



### PCR Listing

To list all 24 PCRs in SHA-256, ensure that the checkbox at (1) is **checked** and select "PCR List All" at (2).

| ![](/images/Optiga_Setup/PCR/TPMPCRSHA256_ListAll.png) |
| ------------------------------------------------------ |

Figure 22: PCR List All 24 Registers in SHA-256

To list all 24 PCRs in SHA-1, ensure that the checkbox at (1) is **unchecked** and select "PCR List All" at (2).  

| ![](/images/Optiga_Setup/PCR/TPMPCRSHA1_ListAll.png) |
| ---------------------------------------------------- |

Figure 23: PCR List All 24 Registers in SHA-1

To list only a specific register out of the 24, we can first choose PCR index at (1). Then select "PCR List" at (2) to display the chosen PCR index. You can also check or uncheck the SHA-256/SHA-1 at (3) as shown below in Figure 24.

| ![](/images/Optiga_Setup/PCR/TPMPCR_ListSpecific.png) |
| ----------------------------------------------------- |

Figure 24: PCR List Specific Register in SHA-1 and SHA-256



### PCR Extend and PCR Event

To perform a PCR Extend, enter an input in the "Input for PCR operations" below and select "PCR Extend". In this example, the default input of "0123456789ABCDEF" is used. Only the bank selected will be extended. 

| ![](/images/Optiga_Setup/PCR/TPMPCR_Extend.png) |
| ----------------------------------------------- |

Figure 25: PCR Extend function

To perform a PCR Event, enter an input in the "Input for PCR operations" below and select "PCR Event". In this example, the default input of "0123456789ABCDEF" is used. Both banks SHA-256 and SHA-1 will be extended as shown in Figure 26.

| ![](/images/Optiga_Setup/PCR/ed1.png) |
| ------------------------------------- |

Figure 26: PCR Event function



## NVM and Certificate Management

This section shows you the functionalities of the NVM and Certificate Management in the OPTIGA™ TPM.

From the "Setup and Basic Features" menu, select the "NVM and Certificate Management".

| ![](/images/Optiga_Setup/NVM/TPMNVM_Screen.png) |
| ----------------------------------------------- |

Figure 27: NVM and Certificate Management Selection

| ![](/images/Optiga_Setup/NVM/NVM_Unedited/TPMNVM_Define.png) |
| ------------------------------------------------------------ |

Figure 28: NVM and Certificate Management Screen



### NVM and Certificate Management Functions

NVM and Certificate Management function descriptions

| ![](/images/Optiga_Setup/NVM/TPMNVM_Screen2.png) |
| ------------------------------------------------ |

Figure 29: OPTIGA™ TPM NVM and Certificate Management Functions Descriptions



### NV Define

Select the NVM attributes and input the NVM index and size. Then select "NV Define" at (1). Then select "NV List" at (2) to check that NVM index 0x1500016 has been defined. Default attrbutes are used in this example.

| ![](/images/Optiga_Setup/NVM/TPMNVM_ScreenSelectdefine.png) |
| ----------------------------------------------------------- |

Figure 30: NV Define and NV List Selection

After selecting "NV List", all defined NVM indexs are shown as seen in Figure 31. NVM index 0x1500016 has been defined as shown by the arrow. In the box, Index 0x1c00002 as well as 0x1c0000a are Infineon EK certificates respectively and **should not** be edited.  

| ![](/images/Optiga_Setup/NVM/TPMNVM_List.png) |
| --------------------------------------------- |

Figure 31: NV List Display



### NV Write

To write in the NV, enter what you wish to input in the NV in the "NVM data". Then select "NV Write" at (1) to write and "NV Read" at (2) to see what you have written.

| ![](/images/Optiga_Setup/NVM/TPMNVM_WritenRead2.png) |
| ---------------------------------------------------- |

Figure 32: NV Write and NV Read display



### Reading Cerificiate

The "ifx_ecc_cert.crt" and the "ifx_rsa_cert.crt" will be created during "Read RSA Cert" and "Read ECC Cert" process. These are the EK Certificates that are inside handles 0x1c00002 and 0x1c0000a respectively.

To read RSA Cert in the NV, ensure that the RSA Cert index is correct and select "Read RSA Cert". In this example, we read the Infineon EK certificate "0x1c00002". A "ifx_rsa_cert.crt" will be created during "Read RSA Cert" process.

| ![](/images/Optiga_Setup/NVM/TPMNVM_ReadRSA.png) |
| ------------------------------------------------ |

Figure 33: Read RSA Cert

To read ECC Cert in the NV, ensure that the ECC Cert index is correct and select "Read ECC Cert". In this example, we read the Infineon EK certificate "0x1c0000a". A "ifx_ecc_cert.crt" will be created during "Read ECC Cert" process.

| ![](/images/Optiga_Setup/NVM/TPMNVM_ReadECC.png) |
| ------------------------------------------------ |

Figure 34: Read ECC Cert



### Writing File

To write, we select "NV Write File" to select a file to write.

| ![](/images/Optiga_Setup/NVM/Write_cert.png) |
| -------------------------------------------- |

Figure 35: NV Write File

For this example, ifx_ecc_cert.crt is selected.

| ![](/images/Optiga_Setup/NVM/TPMNVM_WriteFile.png) |
| -------------------------------------------------- |

Figure 36: NV Write File Selection

The path for the file to be written should be updated. Select "NV Read" to read the file that you have written in.  

| ![](/images/Optiga_Setup/NVM/TPMNVM_WriteFileSuccess.png) |
| --------------------------------------------------------- |

Figure 37: Reading NV Written file

As an ecc cert was written, we can also use "Read ECC Cert" to show the certificate in the proper format.  

| ![](/images/Optiga_Setup/NVM/TPMNVM_WriteFileSuccessInterpreted.png) |
| ------------------------------------------------------------ |

Figure 38: Reading NV written file using Read ECC Cert



### NV Release

To delete an NV index, select "NV Release" at (1). Select "NV List" at (2) to ensure that it is a success. 0x1500016 should be released.

| ![](/images/Optiga_Setup/NVM/TPMNVM_ReleaseSuccess.png) |
| ------------------------------------------------------- |

Figure 39: NV Release and NV List default



## Handle Mangement

This section shows you the functionalities of Handle Management in the OPTIGA™ TPM. The handle management is used to manage all persistent and transient keys in the OPTIGA™ TPM. It is necessary as there is a limit of 3 transient and 7 persistent keys. Hence, handle management can evict persistent keys or flush transient keys to make for more transient and persistent keys.

###  Handle Management Functions

Handle Management function descriptions.

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 40: OPTIGA™ TPM Handle Management Functions Descriptions



### Handle Management List All

From the "Setup and Basic Features" menu, select the "Handle Management".

| ![](/images/Optiga_Setup/Handle_Management/TPM_SetupScreen.png) |
| ------------------------------------------------------------ |

Figure 41: Handle Management Selection

| ![](/images/Optiga_Setup/Handle_Management/HM_Undedited/HM_Main_screen.png) |
| ------------------------------------------------------------ |

Figure 42: Handle Management Screen

Select "List All" to list all persistent handles.

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_LIST.png) |
| ---------------------------------------------------------- |

Figure 43: Handle Management List All Selection

All persistent handles will be listed. You should have no persistent handles shown. Refer to **3.3.2** in order to create a persistent handle. Section 3.3.2 creates a Primary Key which in its process makes the handle 0x81000006 persisted. Once done, it will be listed when selecting the handle management "List all" button.

| ![](/images/Optiga_Setup/Handle_Management/HM_Undedited/TPMHM_ListAll.png) |
| ------------------------------------------------------------ |

Figure 44: Handle Management List All Display

Input a persisted handle and select "Read Persistent" to see the information of the persistent handle selected.  

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_Read.png) |
| ---------------------------------------------------------- |

Figure 45: Handle Management Read Persistent Selection

The information of the persistent handle will shown on the display.

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_ReadPersistent.png) |
| ------------------------------------------------------------ |

Figure 46: Handle Management Read Persistent Display



### Handle Management Evict Persistent

Once a persistent handle is created under section 3.3.2, the persistent handle 0x81000006 can be evicted to make space for more persistent handles.

To evict persistent, input the correct handle value and select "Evict persistent".

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_Evict.png) |
| ----------------------------------------------------------- |

Figure 47: Handle Management Evict Persistent Selection

Enter the set value of the Owner Authorization Value and select "OK" to evict persistent key selected.

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_EvictPersistentHandle_OAV.png) |
| ------------------------------------------------------------ |

Figure 48: Owner Authorization confirmation for evicting persistent handle

Once executed, the persistent handle "0x81000006" should be evicted as seen from Figure 49.

| ![](/images/Optiga_Setup/Handle_Management/TPMHM_EvictPersistentHandle.png) |
| ------------------------------------------------------------ |

Figure 49: Handle Management Evict Persistent List All Screen



# Cryptographic Functions

This section shows you the Cryptographic Functions of the OPTIGA™ TPM. It can be used to hash, encrypt/decrypt or sign and verify using OpenSSL or the TPM2 tools.

Go back to the main screen and select "Cryptographic Functions".

| ![](/images/CryptoFNS/MainScreen_crypto.png) |
| -------------------------------------------- |

Figure 50: OPTIGA TPM 2.0 Explorer Cryptographic Functions Seletcion

| ![](/images/CryptoFNS/TPMCryptoFn_MainScreen.png) |
| ------------------------------------------------- |

Figure 51: Cryptographic Functions Main Screen



## Hash Cryptographic Functions

The hash function in this user interface only supports SHA-256. To hash with another algorithm, you can use "tpm2_hash" command in the terminal.

Select "Hash" in the Cryptographic Functions.

| ![](/images/CryptoFNS/Hash/Select_Hash.png) |
| ------------------------------------------- |

Figure 52: Cryptographic Hash Selection

To hash an input, enter an input and select "Hash (SHA-2).

| ![](/images/CryptoFNS/Hash/TPMCryptoFn_HashSHA2.png) |
| ---------------------------------------------------- |

Figure 53: Cryptographic Hash Display



## RSA Cryptographic Functions

Select "RSA".

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_MainScreen.png) |
| ----------------------------------------------------- |

Figure 54: Cryptogtaphic Functions RSA Selection

| ![](/images/CryptoFNS/RSA/RSA_Unedited/RSAMainscen.png) |
| ------------------------------------------------------- |

Figure 55: Cryptogtaphic Functions RSA Menu



### RSA Cryptographic Function Description

RSA Cryptographic Function Description

| ![](/images/CryptoFNS/RSA/CryptoRSAMain_Screen.png) |
| --------------------------------------------------- |

Figure 56: RSA Cryptographic Function Description



### Creating RSA Keypair

To create RSA keypair, create a primary key first by selecting "Create Primary".

| ![](/images/CryptoFNS/RSA/RSAMainscen2.png) |
| ------------------------------------------- |

Figure 57: RSA Create Primary Selection

Enter the set value of the Owner Authorization Value and select "OK" to create primary key.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSACreatePrimary.png) |
| ----------------------------------------------------------- |

Figure 58: Owner Authorization confirmation for creating primary key

The command tpm2_createprimary will be performed followed by a tpm2_evictcontrol to make it persistent using TPM2 tools as seen in Figure 59. The primary key is created with a parameter 'o' under the storage hierarchy.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSACreatePrimarySuccess.png) |
| ------------------------------------------------------------ |

Figure 59: Cryptogtaphic Functions RSA Create Primary Succeeded

Next, create RSA keypair by selecting "Create RSA Keypair".

| ![](/images/CryptoFNS/RSA/Create_RSA.png) |
| ----------------------------------------- |

Figure 60: Create RSA Keypair Selection

Enter the set value of the Owner Authorization Value and select "OK" to create RSA Keypair.

| ![](/images/CryptoFNS/RSA/x3w.png) |
| ---------------------------------- |

Figure 61: Owner Authorization confirmation for creating RSA Keypair

RSA Keypair successfully created. The command tpm2_create was used to create a RSA key pair under the storage hierarchy. The created key pair was then loaded to the TPM with tpm2_load. Finally, the RSA key was made to be persistent with tpm2_evictcontrol.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSACreateKeypair.png) |
| ----------------------------------------------------------- |

Figure 62: Create RSA Keypair succeeded



### Encrypting and Decrypting RSA

To encrypt an input using RSA key, enter your input and select "RSA Encrypt".

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSAEncrypt.png) |
| ----------------------------------------------------- |

Figure 63: RSA Encrypt

The data has been encrypted.

| ![](/images/CryptoFNS/RSA/RSA_Unedited/TPMCryptoFn_RSAEncryptedData.png) |
| ------------------------------------------------------------ |

Figure 64: Encrypted “data_encrypted.txt” shown in unreadable form

To decrypt encrypted data using RSA key, simply select "RSA Decrypt".

| ![](/images/CryptoFNS/RSA/Decrypto.png) |
| --------------------------------------- |

Figure 65: RSA Decrypt

Data has been decrypted.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSADecrypt.png) |
| ----------------------------------------------------- |

Figure 66: RSA Decrypt succeeded



### Signing and Verifying RSA

To perform RSA Sign, select "RSA Sign".

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSASign.png) |
| -------------------------------------------------- |

Figure 67: RSA Sign

To verify signature using **OpenSSL**, select "RSA Verify (By OpenSSL)". A success message "Verified OK" should be displayed if "Data Input" is correct.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSAVerifybyOSSLSuccess.png) |
| ------------------------------------------------------------ |

Figure 68: RSA signature check with OpenSSL succeeded

If "Data Input" is wrong, an error message "Verification Failure" will be displayed.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSAVerifybyOSSLFail.png) |
| ------------------------------------------------------------ |

Figure 69: RSA signature check with OpenSSL failed

To verify signature using TPM2 tools, select "RSA Verify (By TPM)" to perform a 'tpm2_verifysignature'. No error messages should be displayed if "Data Input" is correct.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSAVerifybyTPMSuccess.png) |
| ------------------------------------------------------------ |

Figure 70: RSA signature check with TPM2 tools succeeded

If "Data Input" is wrong, error messages will be displayed to indicate failure.

| ![](/images/CryptoFNS/RSA/TPMCryptoFn_RSAVerifybyTPMFail.png) |
| ------------------------------------------------------------ |

Figure 71: RSA signature check with TPM2 tools failed



## ECC Cryptographic Functions

Select "ECC".

| ![](/images/CryptoFNS/ECC/SelECC.png) |
| ------------------------------------- |

Figure 72: Cryptographic Functions ECC Selection

| ![](/images/CryptoFNS/ECC/ECC_Unedited/TPMCryptoFn_ECCMainScreen.png) |
| ------------------------------------------------------------ |

Figure 73: Cryptographic Functions ECC Main Screen



### ECC Cryptographic Function Description

ECC Cryptographic Function Description

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCMainScreen.png) |
| -------------------------------------------------------- |

Figure 74: ECC Cryptographic Function Description



### Creating ECC Keypair

To create a ECC keypair, create a primary key first by selecting "Create Primary" to create primary key for ECC.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCCreatePrima.png) |
| --------------------------------------------------------- |

Figure 75: ECC Create Primary

Enter the set value of the Owner Authorization Value and select "OK" to create primary key.

| ![](/images/CryptoFNS/ECC/OwnerAuth.png) |
| ---------------------------------------- |

Figure 76: Owner Authorization confirmation for creating primary key

The command tpm2_createprimary will be performed followed by a tpm2_evictcontrol to make it persistent using TPM2 tools as seen in Figure 77. The primary key is created with a parameter 'o' under the storage hierarchy.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCCreatePrimary.png) |
| ----------------------------------------------------------- |

Figure 77: ECC Create Primary Display

Next, create ECC keypair by selecting "Create ECC Keypair".

| ![](/images/CryptoFNS/ECC/ECC_Sel_Keypair.png) |
| ------------------------------------------------------------ |

Figure 78: Create ECC Keypair Selection

Enter the set value of the Owner Authorization Value and select "OK" to create ECC Keypair.

| ![](/images/CryptoFNS/ECC/OnweAuth_Keypair.png) |
| ----------------------------------------------- |

Figure 79: Owner Authorization confirmation for creating ECC Keypair

ECC Keypair successfully created. The command tpm2_create was used to create a ECC key pair under the storage hierarchy. The created key pair was then loaded to the TPM with tpm2_load. Finally, the ECC key was made to be persistent with tpm2_evictcontrol.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCCreateECCKeypair.png) |
| ------------------------------------------------------------ |

Figure 80: Create ECC Keypair succeeded



### Signing and Verifying ECC

To perform ECC Sign, select "ECC Sign".

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCSign.png) |
| -------------------------------------------------- |

Figure 81: ECC Sign

To verify signature using **OpenSSL**, select "ECC Verify (By OpenSSL)". A success message "Verified OK" should be displayed if "Data Input" is correct.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCVerifyOSSLSuccess.png) |
| ------------------------------------------------------------ |

Figure 82: ECC signature check with OpenSSL succeeded

If "Data Input" is wrong, an error message "Verification Failure" will be displayed.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCVerifyOSSLFail.png) |
| ------------------------------------------------------------ |

Figure 83: ECC signature check with OpenSSL failed

To verify signature using TPM2 tools, select "ECC Verify (By TPM)" to perform a 'tpm2_verifysignature'. No error messages should be displayed if "Data Input" is correct.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCVerifyTPMSuccess.png) |
| ------------------------------------------------------------ |

Figure 84: ECC signature check with TPM2 tools succeeded

If "Data Input" is wrong, error messages will be displayed to indicate failure.

| ![](/images/CryptoFNS/ECC/TPMCryptoFn_ECCVerifyTPMFail.png) |
| ----------------------------------------------------------- |

Figure 85: ECC signature check with TPM failed



# OpenSSL Engine

OpenSSL is an open-source tool that is commonly used for the Transport Layer Security (TLS) protocol. TLS is used by web services and IoT devices to transmit sensitive information between client/Endpoint and Server/Cloud applications.

This section shows you the OpenSSL-Engine functions of the OPTIGA™ TPM. The OpenSSL-Engine can be used to create an RSA/ECC(Client/Server) or do encryption/decryption or signing and verification. It can also be used to to random number generation.

Go back to the main screen and select "OpenSSL-Engine".

| ![](/images/OpenSSL/OSSL_Select.png) |
| ------------------------------------ |

Figure 86: OPTIGA TPM 2.0 Explorer OpenSSL-Engine Selection

| ![](/images/OpenSSL/RSA_Client_Server/RSA_CS_Unedited/TPMOSSL_RSA_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 87: OpenSSL-Engine Main Screen



## RSA (Enc/Dec/Sign/Verify)

This section shows the uses of OpenSSL libraries to do encryption, decryption, signing and verification.

Select "RSA (Enc/Dec/Sign/Verify)".

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_RSA_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 88: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Selection

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/RSA_EDSV_Unedited/TPMOSSL_EDSV_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 89: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Screen



### RSA (Enc/Dec/Sign/Verify) Function Description

RSA (Enc/Dec/Sign/Verify) Function Description

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/X4.png) |
| --------------------------------------------------- |

Figure 90: RSA (Enc/Dec/Sign/Verify) Function Description



#### RSA Encryption and Decryption

To perform RSA functions, select "Generate RSA Keypair". RSA key is generated under storage hierarchy.

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_EDSV_GenerateRSAKeypair.png) |
| ------------------------------------------------------------ |

Figure 91: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Generate RSA Keypair

To encrypt an input, enter an input into "Data Input" and select "RSA Encrypt".

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_EDSV_Encrypt.png) |
| ------------------------------------------------------------ |

Figure 92: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Encrypt

To decrypt, select "RSA Decrypt". Data should be successfully decrypted.

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_EDSV_Decrypt.png) |
| ------------------------------------------------------------ |

Figure 93: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Decrypt



#### RSA Signing and Verification

To sign, enter input in "Data Input" and select "RSA Signing" to sign.

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_EDSV_Signing.png) |
| ------------------------------------------------------------ |

Figure 94: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Signing

To verify, ensure correct "Data Input" and select "RSA Verification".

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_EDSV_VerifySuccess.png) |
| ------------------------------------------------------------ |

Figure 95: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Verify Success

If "Data Input" is wrong, an error message "Verification Failure" will be displayed.

| ![](/images/OpenSSL/RSA_Enc_Dec_Sign_Verify/TPMOSSL_EDSV_VerifyFailure.png) |
| ------------------------------------------------------------ |

Figure 96: OpenSSL-Engine RSA (Enc/Dec/Sign/Verify) Verification Failure



## Random Number Generator

This section shows the use of OpenSSL libraries in generating a random hex or base64 value with indicated no of bytes.

Select "RNG".

| ![](/images/OpenSSL/RNG/TPMOSSL_RSA_MainScreen.png) |
| --------------------------------------------------- |

Figure 97: OpenSSL-Engine RNG Selection

| ![](/images/OpenSSL/RNG/RNG_Unedited/TPMOSSL_RNG_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 98: OpenSSL-Engine RNG Screen

To change the bytes generated, enter the input in "No. of bytes to be generated". To change the encoding of the random number, select the arrow at "Pick encoding of Random Number" and select/<hex> or/<base64>. Select "Generate RNG" to generate random number.

| ![](/images/OpenSSL/RNG/TPMOSSL_RNG_Options.png) |
| ------------------------------------------------ |

Figure 99: OpenSSL-Engine RNG Selection

In Figure 100, the numbers generated are 32 bytes in hex encoding and 64 bytes in base64 encoding.

| ![](/images/OpenSSL/RNG/TPMOSSL_RNG_Generate.png) |
| ------------------------------------------------- |

Figure 100: OpenSSL-Engine RNG Selection



## RSA (Client/Server) 

The RSA(Client/Server) is a demonstration of the hardening of the TLS session between a Client/Endpoint and Server/Cloud the OpenSSL S_Server and S_Client modules will be used along with the local host capability of Linux running on Raspberry Pi® 3B+/4.

TLS provides authenticated key exchange using asymmetric cryptography, data confidentiality using symmetric encryption and message integrity using message authentication codes scheme. However, these crypto primitives are stored in system memory and do not provide any trustworthiness assurance of the involved endpoint.

The drawback is that their implementation is using software library modules that store private keys in

application or secure memory and have proven to contain bugs or vulnerabilities which have been exploited for

the last several years.

The benefit of using SLx 9670 TPM2.0 to protect the private key involved in the TLS handshake process.

### RSA (Client/Server) Function Description

RSA (Client/Server) Function

| ![](/images/OpenSSL/RSA_Client_Server/X2.png) |
| --------------------------------------------- |

Figure 101: RSA (Client/Server) Function Description



### Create Root CA and Its Certificate

At the core of the PKI there is the Root CA where the chain of trust originates. In normal practice you would use an established CA like for example GlobalSign.

For the purpose of this evaluation software we used OpenSSL to create a Root Certificate Authority. This is not advised for production purposes.

**NOTE:** For the OpenSSL Engine, the Owner Authorization Value set should be set as owner123 in order to Generate CA & CA Cert. To set the Owner Authorization Value, refer to section 2.1.4 Changing Authorization values of TPM.

| ![](/images/OpenSSL/RSA_Client_Server/1.png) |
| -------------------------------------------- |

Figure 102: OpenSSL-Engine RSA (Client/Server) Generate CA &amp; CA Cert



### Create Server Certificate

Generate Keypair for server by selecting "Create Keypair (for server)".

| ![](/images/OpenSSL/RSA_Client_Server/2.png) |
| -------------------------------------------- |

Figure 103: OpenSSL-Engine RSA (Client/Server) Create Keypair (for server)

Generate Certificate Signing Request for the Certificate Authority using server private key by selecting "Create CSR".

| ![](/images/OpenSSL/RSA_Client_Server/3.png) |
| -------------------------------------------- |

Figure 104: OpenSSL-Engine RSA (Client/Server) Create CSR

Generate Server Certificate from CSR and CA private key by selecting "Create Server Cert".

| ![](/images/OpenSSL/RSA_Client_Server/4.png) |
| -------------------------------------------- |

Figure 105: OpenSSL-Engine RSA (Client/Server) Create Server Cert



### Create an OpenSSL Server

We will now create an OpenSSL server. For this purpose, we are using the local host capabilities to run this example on the same Linux machine.

Create an openssl server instance using a terminal window session by selecting "Start/Stop Server".

| ![](/images/OpenSSL/RSA_Client_Server/TPMOSSL_RSA_StartServer.png) |
| ------------------------------------------------------------ |

Figure 106: OpenSSL-Engine RSA (Client/Server) Start Server



### Create an OpenSSL Client

We will create an OpenSSL Client and connect through a TLS session with OpenSSL Server (The two terminal windows and services running on the same Linux machine).

The OpenSSL Client will be run and the output of the connection is divided in two parts

a/) The TLS handshake

b/) TLS Cipher

As shown in Figure 107 the complete TLS handshake process was successful, and the encrypted channel established.

| ![](/images/OpenSSL/RSA_Client_Server/TPMOSSL_RSA_StartClient.png) |
| ------------------------------------------------------------ |

Figure 107: OpenSSL-Engine RSA (Client/Server) Start Client



### Secure data exchange between Server and Client

Messages can be sent from Server to Client as well as Client to Server by entering input in the boxes below and selecting "Write to Server" or "Write to Client". The message "Message Hello World Sent from Client" and "Message Hello World Sent from Server" has been successfully sent in Figure 108.

| ![](/images/OpenSSL/RSA_Client_Server/TPMOSSL_RSA_ClientServerCommunication.png) |
| ------------------------------------------------------------ |

Figure 108: OpenSSL-Engine RSA (Client/Server) Communication

To stop connection, end the server by selecting "Start/Stop Server".

| ![](/images/OpenSSL/RSA_Client_Server/TPMOSSL_RSA_StopServer.png) |
| ------------------------------------------------------------ |

Figure 109: OpenSSL-Engine RSA (Client/Server) End Communication



## ECC (Client/Server)

The ECC(Client/Server) is a demonstration to show the use of the TPM Key for secure communications.

Select "ECC (Client/Server)".

| ![](/images/OpenSSL/ECC_Client_Server/ECC_MAin.png) |
| --------------------------------------------------- |

Figure 110: OpenSSL-Engine ECC (Client/Server) Selection



### ECC (Client/Server) Function Description

ECC (Client/Server) Function Description

| ![](/images/OpenSSL/ECC_Client_Server/X3.png) |
| --------------------------------------------- |

Figure 111: ECC (Client/Server) Function Description



### Create Root CA and Its Certificate

At the core of the PKI there is the Root CA where the chain of trust originates. In normal practice you would use an established CA like for example GlobalSign.

For the purpose of this evaluation software we used OpenSSL to create a Root Certificate Authority. This is not advised for production purposes.

**NOTE:** For the OpenSSL Engine, the Owner Authorization Value set should be set as owner123 in order to Generate CA & CA Cert. To set the Owner Authorization Value, refer to section 2.1.4 Changing Authorization values of TPM.

| ![](/images/OpenSSL/ECC_Client_Server/1.png) |
| -------------------------------------------- |

Figure 112: OpenSSL-Engine ECC (Client/Server) Generate CA &amp; CA Cert



### Create Server Certificate

Generate Keypair for server by selecting "Create Keypair (for server)".

| ![](/images/OpenSSL/ECC_Client_Server/2.png) |
| -------------------------------------------- |

Figure 113: OpenSSL-Engine ECC (Client/Server) Create Keypair (for server)

Generate Certificate Signing Request for CA using server private key by selecting "Create CSR".

| ![](/images/OpenSSL/ECC_Client_Server/3.png) |
| -------------------------------------------- |

Figure 114: OpenSSL-Engine ECC (Client/Server) Create CSR

Generate Server Certificate from CSR and CA private key by selecting "Create Server Cert".

| ![](/images/OpenSSL/ECC_Client_Server/4.png) |
| -------------------------------------------- |

Figure 115: OpenSSL-Engine ECC (Client/Server) Create Server Cert



### Create an OpenSSL Server

We will now create an OpenSSL server. For this purpose, we are using the local host capabilities to run this example on the same Linux machine.

Create an openssl S_Server instance using a terminal window session by selecting "Start/Stop Server".

| ![](/images/OpenSSL/ECC_Client_Server/Start_server.png) |
| ------------------------------------------------------- |

Figure 116: OpenSSL-Engine ECC (Client/Server) Start Server



### Creating an OpenSSL Client

We will create an OpenSSL Client and connect through a TLS session with OpenSSL Server (The two terminal windows and services running on the same Linux machine).

The OpenSSL Client will be run and the output of the connection is divided in two parts

a/) The TLS handshake

b/) TLS Cipher

As shown in Figure 117 the complete TLS handshake process was successful, and the encrypted channel

| ![](/images/OpenSSL/ECC_Client_Server/Start_Client.png) |
| ------------------------------------------------------- |

Figure 117: OpenSSL-Engine ECC (Client/Server) Start Client



### Secure data exchange between Server and client

Messages can be sent from Server to Client as well as Client to Server by entering input in the boxes below and selecting "Write to Server" or "Write to Client". The message "Message Hello World Sent from Client" and "Message Hello World Sent from Server" has been successfully sent in Figure 118.

| ![](/images/OpenSSL/ECC_Client_Server/TPMOSSL_ECC_ClientServerCommunication.png) |
| ------------------------------------------------------------ |

Figure 118: OpenSSL-Engine ECC (Client/Server) Communication

To stop connection, end the server by selecting "Start/Stop Server".

| ![](/images/OpenSSL/ECC_Client_Server/TPMOSSL_ECC_StopServer.png) |
| ------------------------------------------------------------ |

Figure 119: OpenSSL-Engine ECC (Client/Server) End Communication



# Data Sealing with Policy

This section shows you the Data Sealing with Policy in the OPTIGA™ TPM. It can be used to seal data using a PCR policy.

Sealing permits the key or secret to be protected not only by a password but by a policy. A typical policy locks the key to PCR values (the software state) current at the time of sealing. This assumes that the state at first boot is not compromised. Any preinstalled malware present at first boot would be measured into the PCRs, and thus the key would be sealed to a compromised software state.

## Data Sealing with Policy Function Description

Data Sealing with Policy Function Description

| ![](/images/Data_Sealing_with_Policy/TPMEA_MainScreen.png) |
| ---------------------------------------------------------- |

Figure 120: Data Sealing with Policy Function Description



## Data Sealing with Policy Functions

Go back to the main screen and select "Data Sealing with Policy".

| ![](/images/Data_Sealing_with_Policy/MainScreen.png) |
| ---------------------------------------------------- |

Figure 121: OPTIGA TPM 2.0 Explorer Data Sealing with Policy Selection

| ![](/images/Data_Sealing_with_Policy/DataSealingWPolicy_Unedited/TPMEA_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 122: Data Sealing with Policy Screen



### Data Sealing with Policy

Select PCR Index and generate policy by selecting "Generate Policy from selected PCR". In this example, PCR Index "5" will be used. The policy will be tied down to PCR 5 and its predefined value.

| ![](/images/Data_Sealing_with_Policy/TPMEA_GeneratePolicy.png) |
| ------------------------------------------------------------ |

Figure 123: Data Sealing with Policy Generate Policy

Select "Generate Primary (Owner)" to generate primary key under storage hierarchy and the Owner Authorization Value will be prompted. Enter the Owner Authorization Value and select "OK" to proceed.

| ![](/images/Data_Sealing_with_Policy/TPMEA_GeneratePrimary.png) |
| ------------------------------------------------------------ |

Figure 124: Data Sealing with Policy Generate Primary (Owner)

Once "OK" is selected, a primary key will be created and the handle will be persisted under the storage hierarchy.

| ![](/images/Data_Sealing_with_Policy/DataSealingWPolicy_Unedited/TPMEA_GeneratePrimary.png) |
| ------------------------------------------------------------ |

Figure 125: Data Sealing with Policy Generate Primary (Owner)

Enter an input in "Data to be sealed". Then select "Seal Data" to seal the input.

| ![](/images/Data_Sealing_with_Policy/TPMEA_Seal.png) |
| ---------------------------------------------------- |

Figure 126: Data Sealing with Policy Seal Data

To unseal data, ensure that the PCR Index is correct and select "Satisfy Policy and Unseal".

| ![](/images/Data_Sealing_with_Policy/TPMEA_UnsealSuccess.png) |
| ------------------------------------------------------------ |

Figure 127: Data Sealing with Policy Satisfy Policy and Unseal Success

If PCR index is wrong, policy check will fail as the predefined PCR index is 5.

| ![](/images/Data_Sealing_with_Policy/TPMEA_UnsealFail.png) |
| ---------------------------------------------------------- |

Figure 128: Data Sealing with Policy Satisfy Policy and Unseal Failure with wrong PCR index

If PCR index is correct but value is wrong, error messages will be displayed to indicate failure as the predefined value of PCR index 5 is all '0x0000000000000000000000000000000000000000000000000000000000000000'. First, we head go to Setup and Basic Features under PCR to extend PCR index 5. Refer to Section 2.2.3 for information on extend PCR.

| ![](/images/Data_Sealing_with_Policy/x1.png) |
| -------------------------------------------- |

Figure 129: Extending PCR Index 5 with Setup and Basic Features PCR

If PCR index is correct but value is wrong, an error message that the PCR value is wrong will be shown and the policy check will fail. TPM2_unseal will not be successful.

| ![](/images/Data_Sealing_with_Policy/x2.png) |
| -------------------------------------------- |

Figure 130: Data Sealing with Policy Satisfy Policy and Unseal with right PCR index and wrong index value



# Attestation

This section shows you how to use Attestation in the OPTIGA™ TPM. A system health check supported by Infineon's OPTIGA™ TPM lets users check that their devices have not been manipulated. The TPM provides a secured identity and storage space for system control mechanisms that may check whether hardware and software are still running as intended. The system notifies the user if it does detect changes, e.g. caused by malware.

Go back to the main screen and select "Attestation".

| ![](/images/Attestation/MainScreen.png) |
| --------------------------------------- |

Figure 131: OPTIGA TPM 2.0 Explorer Attestation Selection

| ![](/images/Attestation/Attestation_Unedited/TPMAttestation_MainScreen.png) |
| ------------------------------------------------------------ |

Figure 132: OpenSSL-Engine Attestation Main Screen



## Attestation Function Description

A TPM attestation offers cryptographic proof of software state. The attestation is a TPM quote: a number of PCR are hashed, and that hash is signed by a TPM key known as attestation key. If the remote party can validate that the signing key came from an authentic TPM, it can be assured that the PCR digest report has not been altered. The device remote attestation supported by Infineon's OPTIGA™ TPM lets users check that their devices have not been manipulated to establish the trust in the devices.

| ![](/images/Attestation/TPMAttestation_MainScreen.png) |
| ------------------------------------------------------ |

Figure 133: Attestation Function Description



## Generating Quote

To generate a signing key, AK will be required. An AK can be generated from an EK. If an EK has not been generated, select the button “Generate EK, if applicable” to generate an endorsement key using RSA. 

| ![](/images/Attestation/TPMAttestation_SELGenerateEK.png) |
| --------------------------------------------------------- |

Figure 134: Attestation Select Generate EK

Enter the set value of the Owner Authorization Value and select “OK” to create Generate EK.

| ![](/images/Attestation/TPMAttestation_Owner.png) |
| ------------------------------------------------- |

Figure 135: Owner Authorization confirmation for generating EK

Enter the set value of the Endorsement Authorization Value and select “OK” to create Generate EK.

| ![](/images/Attestation/TPMAttestation_Endorsement.png) |
| ------------------------------------------------------- |

Figure 136: Endorsement Authorization confirmation for generating EK

EK will be successfully generated.

| ![](/images/Attestation/TPMAttestation_GenerateEK.png) |
| ------------------------------------------------------ |

Figure 137: EK Generated

Then, select “Generate AK from EK” to generate Attestation Keypair from the Endorement Key.[[LN(DSAEI1/]](#_msocom_1) 

| ![](/images/Attestation/TPMAttestation_SELGenerateAKfromEK.png) |
| ------------------------------------------------------------ |

Figure 138: Attestation Select Generate AK from EK

Enter the set value of the Owner Authorization Value and select “OK” to Generate AK from EK.

| ![](/images/Attestation/TPMAttestation_GenerateAKfromEK_Owner.png) |
| ------------------------------------------------------------ |

Figure 139: Owner Authorization confirmation for generating AK from EK

Enter the set value of the Endorsement Authorization Value and select “OK” to Generate AK from EK.

| ![](/images/Attestation/TPMAttestation_GenerateAKfromEK_Endorsement.png) |
| ------------------------------------------------------------ |

Figure 140: Endorsement Authorization confirmation for generating AK from EK

AK will be successfully generated.

| ![](/images/Attestation/TPMAttestation_GenerateAKfromEK.png) |
| ------------------------------------------------------------ |

Figure 141: AK Generated

Configure the "PCR 256 Index" to the index you wish to perform the signing. In this example, we will use PCR Index 5.

Next, Select the button "Generate Quote". The PCR is signed by TPM attestation key. The Nonce used in this specific example to generate quote will be "9e0c6f", an even number of hexadecimal symbols and will be converted into a byte array, but in real life application, the nonce will be a random or pseudo-random number issued in an authentication protocol to ensure that old communications cannot be reused in replay attacks.

| ![](/images/Attestation/TPMAttestation_GenerateQuote.png) |
| --------------------------------------------------------- |

Figure 142: Attestation Generate Quote



## Verifying Quote

To verify quote using OpenSSL, select "Verify Quote (OpenSSL)". A "Verified OK" message will be displayed upon success. To verify quote using TPM2 Tools, select "Verify Quote (TPM)". A command tpm2_checkquote will be issued to check for discrepancies from the generation of quote and no error messages will be displayed if successful. RSA Signature will be checked during verification.

| ![](/images/Attestation/TPMAttestation_VerifyOSSL_TPM.png) |
| ---------------------------------------------------------- |

Figure 143: Attestation Verify Quote with OpenSSL and TPM2 Tools Success

For the Attestation verification for Quote of (TPM), in this example of the TPM Explorer, the "Nonce" is changed to be "aaaaaabb". If the server uses a difference "Nonce" than the one used during quote generation "9e0c6f", error messages will be displayed to indicate failure.

| ![](/images/Attestation/fail.png) |
| --------------------------------- |

Figure 144: Attestation Verify Quote TPM Failure



## Evict AK/EK Handle

If you need to evict AK/EK Handle in order to make space for more persistent handles, input the handle to evict correctly and select "Evict AK/EK handle".

| ![](/images/Attestation/TPMAttestation_Evict.png) |
| ------------------------------------------------- |

Figure 145: Attestation Evict AK/EK Handle

Enter the set value of the Owner Authorization Value and select “OK” to Evict AK/EK Handle.

| ![](/images/Attestation/TPMAttestation_Evict_Owner.png) |
| ------------------------------------------------------- |

Figure 146: Owner Authorization confirmation for Evicting AK/EK handle

Persistent-handle: 0x81010002 should be successfully evicted.

| ![](/images/Attestation/TPMAttestation_Evict.png) |
| ------------------------------------------------- |

Figure 147: Evicting AK/EK handle Success



# <a name="secured-connection-to-aws-iot-core-using-tpm2.0"></a>Secured connection to AWS IoT core using TPM2.0

AWS IoT core makes use of X.509 certificates to authenticate client or device connections during a registration and onboading attempt.

The "Application: Cloud Connectivity" demo example showcases how to set up trusted connection to AWS IoT core using X.509 with a TPM2.0 private key. The demo software was developed using the AWS IoT Device SDK for Embedded C, integrating OPTIGA™ TPM2.0 into the platform.

This section explains the following steps required to run the demo
1.  Get started with AWS IoT core
2.  Create device certificate and assign it to Thing with policy
3.  Publish messages to AWS IoT core from the Raspberry Pi

Go back to the main screen and select "Application: Cloud Connectivity".

| ![](/images/AWSIOT/MainScreen.png) |
| ---------------------------------- |

Figure 148: OPTIGA TPM 2.0 Explorer Application: Cloud Connectivity Selection

| ![](/images/AWSIOT/AWSIOT_Unedited/AWS_Main2.png) |
| ------------------------------------------------- |

Figure 149: AWS Cloud Connectivity Main Screen



## Get started with AWS IoT Core

To generate "Access Key ID" and "Secret Access Key", log in to AWS IOT at: "https://infineonap.signin.aws.amazon.com/console".

| ![](/images/AWSIOT/AWSIOT_Unedited/Cloud/AWS_Signin.png) |
| -------------------------------------------------------- |

Figure 150: AWS IOT Login

Next, go to your security credentials.

| ![](/images/AWSIOT/AWSIOT_Unedited/Cloud/security_cred.jpg) |
| ----------------------------------------------------------- |

Figure 151: AWS IOT Security Credentials

Download your security credentials.

| ![](/images/AWSIOT/AWSIOT_Unedited/Cloud/Download_Create_Access_Key.jpg) |
| ------------------------------------------------------------ |

Figure 152: AWS IOT Download Security Credentials


| ![](/images/AWSIOT/AWSIOT_Unedited/Credentials.png) |
| --------------------------------------------------- |

Figure 153: Security_Credentials.CSV


To retrieve Endpoint, go to "Services" and select "IOT Core".

| ![](/images/AWSIOT/AWSIOT_Unedited/Cloud/Services_iotcore.jpg) |
| ------------------------------------------------------------ |

Figure 154: AWS IOT Core

Select "Settings" at the left side of the webbrowser.

| ![](/images/AWSIOT/AWSIOT_Unedited/Cloud/IOT_core_settings.jpg) |
| ------------------------------------------------------------ |

Figure 155: AWS IOT Core Settings

At "Custom Endpoint", copy the endpoint.

| ![](/images/AWSIOT/AWSIOT_Unedited/Cloud/Endpt.jpg) |
| --------------------------------------------------- |

Figure 156: AWS IOT Core Settings Endpoint

Input the "Access Key ID" and "Secret Access Key".

| ![](/images/AWSIOT/Credentials_entered.png) |
| ------------------------------------------- |

Figure 157: AWS IOT Configuration

Change the region to "us-east-2" and select "Set AWS credentials".

| ![](/images/AWSIOT/Credentials_entered2.png) |
| -------------------------------------------- |

Figure 158: AWS IOT Set AWS Credentials Selection

**Skip this step if a policy file has already been created.** First, select "Open policy file", make no changes and save. This is a one time setting only.

| ![](/images/AWSIOT/AWS_Main3.png) |
| --------------------------------- |

Figure 159: AWS IOT Open Policy File Selection

| ![](/images/AWSIOT/AWSIOT_Unedited/policyfille.png) |
| --------------------------------------------------- |

Figure 160: AWS IOT Policy File

Next, set Endpoint by selecting "Open config file".

| ![](/images/AWSIOT/AWS_Main2.png) |
| --------------------------------- |

Figure 161: AWS IOT Open Config File Selection

Paste the endpoint from the custom endpoint copied from AWS IOT Core Settings Endpoint and save.

| ![](/images/AWSIOT/Endpoint_editing.png) |
| ---------------------------------------- |

Figure 162: AWS IOT Open Config File

Select "Create Policy (from policy file)". Once policy has been created, there will be no need to do this step again.

| ![](/images/AWSIOT/AWS_Create_Policy.png) |
| ----------------------------------------- |

Figure 163: AWS IOT Create Policy Selection



## Create device certificate and assign it to Thing with policy

Once configuration is done, to provision the certificate, select "1-click provision". Step 1 to Step 6 will be run and a certificate will be generated after receiving the CSR based on keys generated in the TPM, using AWS IoT's certificate authority.

The following code will be run for Step 1 to Step 6.

```
Step 1: Generate a new key pair from TPM2.0 and export the public key.

(/'/>/>/>/',/'tpm2tss-genkey -o owner123 -a rsa rsa.tss/')

Step 2: Generate a Certificate Signing Request

(/'/>/>/>/', u/'openssl req -new -config temp.conf -engine tpm2tss -key rsa.tss -keyform engine -subj/CN=AWS_IoT_TPM_Certificate/O=Infineon_Technologies/C=SG/ST=Singapore -out leaf.csr/')

Step 3: Create AWS IoT Thing

(/'/>/>/>/', u/'aws iot create-thing/--thing-name TPM_UI_Demo/')

Step 4: AWS IoT constructs a new certificate based on the CSR and signs it with the ATS endpoint CA

(/'/>/>/>/',/'aws iot create-certificate-from-csr/--certificate-signing-request file://leaf.csr/--set-as-active/--certificate-pem-outfile leafAWS.crt/')

Step 5: Attach AWS IoT Certificate to AWS IoT Thing

(/'/>/>/>/', u/'aws iot attach-thing-principal/--thing-name TPM_UI_Demo/--principal arn:aws:iot:us-east-2:065398228892:cert/2e3ee116ee7927525e106b3a9579e83e6b879921200fcf056d132be3ea42d623/')

Step 6: The policy is attached to the received certificate

(/'/>/>/>/', u/'aws iot attach-policy/--policy-name IoT_Publish_Subscribe/--target arn:aws:iot:us-east-2:065398228892:cert/2e3ee116ee7927525e106b3a9579e83e6b879921200fcf056d132be3ea42d623/')
```

| ![](/images/AWSIOT/AWSIOT_Unedited/AWS_Main3.png) |
| ------------------------------------------------- |

Figure 164: AWS IOT 1-click provision Selection

1-click provision is successful if no error message is seen and certificate is successfully attached as shown in Figure 165. Data can now be sent to AWS webbrowser.

| ![](/images/AWSIOT/extra.png) |
| ----------------------------- |

Figure 165: AWS IOT 1-click provision Succeeded



## Publish messages to AWS IoT core from the Raspberry Pi

After performing all the necessary preparation steps from Step 1 to Step 6, we will set up the topic for the AWS webbrowser for the TPM Explorer to publish the data to. Return to the AWS IOT webbrowser. Select "Test" on the left tab. Then enter "pulsioximeter" and select "Subscribe".

| ![](/images/AWSIOT/Suscibe.png) |
| ------------------------------- |

Figure 166: AWS IOT Test

We can proeed with Step 7. On the OPTIGA™ TPM Explorer AWS IOT, input the correct Topic and the intended Data. Then, select "Start Publishing". The device can continue publishing even after reboot and no further configuration will be required.

| ![](/images/AWSIOT/publish.png) |
| ------------------------------- |

Figure 167: AWS IOT Start Publishing Selection

On the AWS IOT webbrowser, subscription to "pulsioximeter" should be shown and an update of the data will be published as shown in Figure 168. This example can be used in many other real time applications where the data can be continuously published to the AWS Iot webbrowser.

| ![](/images/AWSIOT/publiushed.png) |
| ---------------------------------- |

Figure 168: AWS IOT WebBrowser Successfully Published



## <a name="references"></a>References

1.  https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2022-01-28/
2.  <https://www.infineon.com/cms/en/product/evaluation-boards/iridium9670-tpm2.0-linux/>
3.  <http://www.infineon.com/tpm>
4.  https://trustedcomputinggroup.org/resource/tpm-main-specification/



