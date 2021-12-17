#!/bin/sh
set -e
sudo apt update 
sudo apt -y install autoconf-archive awscli libcmocka0 libcmocka-dev procps iproute2 build-essential git pkg-config gcc libtool automake libssl-dev uthash-dev autoconf doxygen libgcrypt-dev libjson-c-dev libcurl4-gnutls-dev uuid-dev pandoc libglib2.0-dev libsqlite3-dev libyaml-dev python-wxtools
wget http://ftpmirror.gnu.org/autoconf-archive/autoconf-archive-2019.01.06.tar.xz -P $PWD/
tar -xf $PWD/autoconf-archive-2019.01.06.tar.xz -C $PWD/
git clone https://github.com/tpm2-software/tpm2-tss.git $PWD/tpm2-tss
cd $PWD/tpm2-tss/
git checkout 23a264b041e836a0e485f7c10e1da2e2bce6bd6c
cd ..
sudo cp -r $PWD/autoconf-archive-2019.01.06/m4 $PWD/tpm2-tss/
cd $PWD/tpm2-tss/

./bootstrap
./configure --with-udevrulesdir=/etc/udev/rules.d
make -j$(nproc) 
sudo make install 
sudo ldconfig
cd ..
git clone https://github.com/tpm2-software/tpm2-tools.git $PWD/tpm2-tools/
cd $PWD/tpm2-tools/
git checkout 961f8b5e21101ed0130ca2edf496312ab1b36961
./bootstrap
cd ..
sudo cp -r $PWD/autoconf-archive-2019.01.06/m4 $PWD/tpm2-tools/
cd $PWD/tpm2-tools/
./bootstrap
./configure
make -j$(nproc) 
sudo make install 
sudo ldconfig
cd ..
git clone https://github.com/tpm2-software/tpm2-abrmd $PWD/tpm2-abrmd/
cd $PWD/tpm2-abrmd/
git checkout 1beda7906dd959bfa53f39ca58f66bea073fa58c
cd ..
sudo cp -r $PWD/autoconf-archive-2019.01.06/m4 $PWD/tpm2-abrmd/
cd $PWD/tpm2-abrmd/
./bootstrap 
./configure --with-dbuspolicydir=/etc/dbus-1/system.d
make -j$(nproc) 
sudo make install 
sudo ldconfig
cd ..
sudo useradd --system --user-group tss
sudo pkill -HUP dbus-daemon
sudo systemctl daemon-reload
git clone https://github.com/tpm2-software/tpm2-tss-engine $PWD/tpm2-tss-engine/
cd $PWD/tpm2-tss-engine/
git checkout 2da48e4ceadc91a7198136309a81b8611327bdf3
cd ..
sudo cp -r $PWD/autoconf-archive-2019.01.06/m4 $PWD/tpm2-tss-engine/
cd $PWD/tpm2-tss-engine/
./bootstrap 
./configure 
make -j$(nproc) 
sudo make install 
sudo ldconfig
cd ..
cd $PWD/Python_TPM20_GUI/
sudo chmod a+rwx create_binary_package.sh 
./create_binary_package.sh
cd bin/
sudo reboot
