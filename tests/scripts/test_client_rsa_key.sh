#!/bin/sh

# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

set -e


openssl s_client -connect localhost:4433 -tls1_3 -CAfile CA_rsa_cert.pem
