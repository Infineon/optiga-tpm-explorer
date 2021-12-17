#!/bin/sh
cd /home/pi/Python_TPM20_GUI/;

sudo rm -r shell_util.py
echo 'import subprocess
import os
from subprocess import PIPE

# Variables to hold the 3 authorisation values' >> shell_util.py
cat /home/pi/Python_TPM20_GUI/bin/working_space/values.txt >> shell_util.py


./create_binary_package.sh
#cd /home/pi/Python_TPM20_GUI/bin/;
#./start_gui.sh