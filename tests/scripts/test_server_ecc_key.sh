#!/bin/sh

# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

set -e


#Generate CA RSA key and Certificate
openssl genpkey -algorithm EC -out ec_CA_key.pem -pkeyopt ec_paramgen_curve:P-384
openssl req -key ec_CA_key.pem -new -x509 -days 7300 -sha256   -out CA_ecc_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=CSS/CN=TPMEvalKitCA'

#Create primary key
set +e
tpm2_evictcontrol -C o -c 0x8100000B -P owner123
set -e
tpm2_createprimary -C o -P owner123 -g sha256 -G ecc -c ECCprimary1.ctx
tpm2_evictcontrol -C o -c ECCprimary1.ctx -P owner123 0x8100000B

#Generate Server key with TPM
openssl req -new -provider tpm2  -pkeyopt parent:0x8100000B -subj /CN=TPM_UI/O=Infineon/C=SG -out server_ecc.csr -keyout ecc_server_tss.pem

#Generate Server certificate
openssl x509 -req -in server_ecc.csr -CA CA_ecc_cert.pem -CAkey ec_CA_key.pem -out CAsigned_ecc_cert.crt -days 365 -sha256 -CAcreateserial 

openssl s_server -provider tpm2 -provider default -cert CAsigned_ecc_cert.crt -accept 4432  -key ecc_server_tss.pem 
