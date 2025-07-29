#!/bin/sh

# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

set -e


#Generate CA RSA key and Certificate
openssl genpkey -algorithm RSA -out rsa_CA.pem
openssl req -key rsa_CA.pem -new -x509 -days 7300 -sha256   -out CA_rsa_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=CSS/CN=TPMEvalKitCA'

#Create primary key
set +e
tpm2_evictcontrol -C o -c 0x8100000A -P owner123
set -e
tpm2_createprimary -C o -P owner123 -g sha256 -G ecc -c ECCprimary.ctx
tpm2_evictcontrol -C o -c ECCprimary.ctx -P owner123 0x8100000A

#Generate Server key with TPM
openssl req -new -provider tpm2  -pkeyopt parent:0x8100000A -subj /CN=TPM_UI/O=Infineon/C=SG -out server_rsa.csr -keyout rsa_server_tss.pem

#Generate Server certificate
openssl x509 -req -in server_rsa.csr -CA CA_rsa_cert.pem -CAkey rsa_CA.pem -out CAsigned_rsa_cert.crt -days 365 -sha256 -CAcreateserial 

openssl s_server -provider tpm2 -provider default -cert CAsigned_rsa_cert.crt -accept 4433  -key rsa_server_tss.pem 
