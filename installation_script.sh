#!/bin/sh

# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

CONFIG_FILENAME="/boot/firmware/config.txt"
TPM_SPI_OVERLAY="dtoverlay=tpm-slb9670"
TPM_I2C_OVERLAY="dtoverlay=tpm-slb9673"
SPI_OVERLAY_OFF="dtparam=spi=off"
SPI_OVERLAY_ON="dtparam=spi=on"
I2C_OVERLAY_OFF="dtparam=i2c_arm=off"
I2C_OVERLAY_ON="dtparam=i2c_arm=on"

set -e

# Install required packages for TPM and GUI
sudo apt update 
sudo apt --yes install libtss2-* tpm-udev tpm2-abrmd tpm2-tools tpm2-openssl python-wxtools xxd python3-pubsub

# Add current user to tss group
sudo usermod --append --groups tss $(whoami)
BASEDIR=$(realpath $(dirname $0))
# Build the Python TPM GUI binary
cd $PWD/src/Python_TPM20_GUI/
sudo chmod a+rwx create_binary_package.sh 
./create_binary_package.sh
set +e
sudo rm ${BASEDIR}/start_gui.sh 2> /dev/null
set -e
sudo ln -s ${BASEDIR}/src/Python_TPM20_GUI/bin/start_gui.sh  ${BASEDIR}/start_gui.sh

# Modify config.txt if it exists
if [ -f "$CONFIG_FILENAME" ]; then
    echo "Found file $CONFIG_FILENAME."
    # Ensure both TPM overlays are present
    # Add SPI TPM overlay
    if ! grep -q "$TPM_SPI_OVERLAY" "$CONFIG_FILENAME"; then
	echo "$TPM_SPI_OVERLAY" | sudo tee -a "$CONFIG_FILENAME"
	echo "Added '$TPM_SPI_OVERLAY' to $CONFIG_FILENAME."
    else
        echo "'$TPM_SPI_OVERLAY' exists in $CONFIG_FILENAME."
    fi
    # Add I2C TPM overlay
    if ! grep -q "$TPM_I2C_OVERLAY" "$CONFIG_FILENAME"; then
	echo "$TPM_I2C_OVERLAY" | sudo tee -a "$CONFIG_FILENAME"
	echo "Added '$TPM_I2C_OVERLAY' to $CONFIG_FILENAME."
    else
        echo "'$TPM_I2C_OVERLAY' exists in $CONFIG_FILENAME."
    fi
    
    # Enable SPI by replacing 'off' with 'on', or appending if neither found
    if grep -q "$SPI_OVERLAY_ON" "$CONFIG_FILENAME"; then
        echo "'$SPI_OVERLAY_ON' already exists in $CONFIG_FILENAME."
    else
        if grep -q "$SPI_OVERLAY_OFF" "$CONFIG_FILENAME"; then
            sudo sed -i "s/$SPI_OVERLAY_OFF/$SPI_OVERLAY_ON/g" "$CONFIG_FILENAME"
            echo "Replaced '$SPI_OVERLAY_OFF' with '$SPI_OVERLAY_ON'."
        else
            echo "$SPI_OVERLAY_ON" | sudo tee -a "$CONFIG_FILENAME"
            echo "'$SPI_OVERLAY_ON' has been appended to $CONFIG_FILENAME."
        fi
    fi

    # Enable I2C by replacing 'off' with 'on', or appending if neither found
    if grep -q "$I2C_OVERLAY_ON" "$CONFIG_FILENAME"; then
        echo "'$I2C_OVERLAY_ON' already exists in $CONFIG_FILENAME."
    else
        if grep -q "$I2C_OVERLAY_OFF" "$CONFIG_FILENAME"; then
            sudo sed -i "s/$I2C_OVERLAY_OFF/$I2C_OVERLAY_ON/g" "$CONFIG_FILENAME"
            echo "Replaced '$I2C_OVERLAY_OFF' with '$I2C_OVERLAY_ON'."
        else
            echo "$I2C_OVERLAY_ON" | sudo tee -a "$CONFIG_FILENAME"
            echo "'$I2C_OVERLAY_ON' has been appended to $CONFIG_FILENAME."
        fi
    fi

else
    echo "The file $CONFIG_FILENAME does not exist. Enable the SPI/I2C and TPM overlays manually needed"
    exit
fi

sudo reboot
