#!/bin/sh

# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

set -e

echo "Preparing release"
cd ../..
rm -rf *.gz
COMMIT_SHA=$(git rev-parse --short HEAD)
echo "$COMMIT_SHA"
tar --exclude='.*' -czf optiga_tpm_explorer_$COMMIT_SHA.tar.gz *

echo " release package done $PWD/optiga_tpm_explorer_$COMMIT_SHA.tar.gz "

