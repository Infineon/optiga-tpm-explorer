# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

import subprocess
import os
from subprocess import PIPE
import json

# Variables to hold the 3 authorisation values
ownerAuth = ""
nvAuth = ""
endorseAuth = ""
lockoutAuth = ""
openssl_cnf = (
    "openssl_conf = openssl_init\n"
    "[openssl_init]\n"
    "providers = provider_sect\n"
    "[provider_sect]\n"
    "default = default_sect\n"
    "tpm2 = tpm2_sect\n"
    "SET_OWNERAUTH = %s\n"
    "[default_sect]\n"
    "activate = 1\n"
    "[tpm2_sect]\n"
    "activate = 1\n"
    # "default_algorithms = ALL\n"
    "[req]\n"
    "distinguished_name = subject\n"
    "[subject]\n" % ownerAuth
)


def convertInputToHex(input_str, req_length):
    converted_output = ""
    # convert input to hex
    # L has to be stripped due to some weird python convention
    # [2:] as the first two are the hex prefix, 0x
    try:
        converted_output += ((hex(int(input_str, 16)))[2:]).strip("L")
    except ValueError:
        return 0
    # if input is still too short, pad with zeroes
    # if too long, truncate to appropriate length
    diff_length = req_length - len(converted_output)
    if diff_length > 0:
        while diff_length > 0:
            converted_output += "0"
            diff_length -= 1
    return converted_output[:req_length]


def checkDir():
    workingDir = "./working_space/"
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)
    os.chdir(workingDir)
    return


# Executes the supplied shell script on the command line
def execShellScript(fullpath):
    output = ""
    try:
        print(input)
        output = subprocess.check_output([sh, str(fullpath)], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output.decode())
    return output.decode()


# Executes a command on the command line
def execTpmToolsAndCheck(cmd, allowFail=True):
    output = ""

    try:
        print((">>> ", " ".join(cmd)))
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
        print(("{0} returned {1}".format(cmd[0], e.returncode)))
    if ("error" in str(output).lower()) or ("fail" in str(output).lower()):
        if not allowFail:
            print(("ERROR in {0}".format(cmd[0])))
            print((str(output)))
            exit()

    print((str(output.decode())))
    return output.decode()


# Executes the supplied command parameters with OpenSSL
def execCLI(cmd):
    output = ""
    try:
        print((">>> ", " ".join(cmd)))
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output.decode())
    return output.decode()


def createProcess(cmd, file):
    output = ""
    try:
        output = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT
        )

    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)

    return output


def createProcess_PIPE(cmd, file):
    output = ""
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)
    return output


def get_auth_from_config(auth_type):
    # Get auth values from config file or reset if file doesn't exist.
    try:
        with open("tpm_auth.json", "r") as f:
            config = json.load(f)

            # Map auth_type to config key
            auth_map = {
                "owner": "ownerAuth",
                "endorse": "endorseAuth",
                "lockout": "lockoutAuth",
                "nv": "nvAuth",
            }

            if auth_type not in auth_map:
                print(
                    f"Invalid auth_type: {auth_type}. Use owner, endorse, lockout or nv as auth_type."
                )
                return None

            return config.get(auth_map[auth_type], "")

    except FileNotFoundError:
        # If config doesn't exist, clear TPM and create empty config
        execTpmToolsAndCheck(["tpm2_clear", "-c", "p"])
        # Set all module variables to empty
        global ownerAuth, endorseAuth, lockoutAuth, nvAuth
        ownerAuth = endorseAuth = lockoutAuth = nvAuth = ""
        save_auth_values()
        return ""
    except json.JSONDecodeError:
        print("Error reading config file")
        return None


def save_auth_values():
    values = {
        "ownerAuth": ownerAuth,
        "endorseAuth": endorseAuth,
        "lockoutAuth": lockoutAuth,
        "nvAuth": nvAuth,
    }
    try:
        with open("tpm_auth.json", "w") as f:
            json.dump(values, f, indent=2)
    except Exception as e:
        print(f"Error saving auth values: {e}")


def save_partial_auth(ownerAuth=None, endorseAuth=None, lockoutAuth=None, nvAuth=None):
    # Load existing values from the JSON file if it exists
    try:
        with open("tpm_auth.json", "r") as f:
            values = json.load(f)
    except FileNotFoundError:
        # If config doesn't exist, clear TPM and create empty config
        execTpmToolsAndCheck(["tpm2_clear", "-c", "p"])
        ownerAuth = endorseAuth = lockoutAuth = nvAuth = ""
        save_auth_values()
        return ""

    # Update values only if a new value is provided
    if ownerAuth is not None:
        values["ownerAuth"] = ownerAuth
    if endorseAuth is not None:
        values["endorseAuth"] = endorseAuth
    if lockoutAuth is not None:
        values["lockoutAuth"] = lockoutAuth
    if nvAuth is not None:
        values["nvAuth"] = nvAuth

    # Save updated values back to the JSON file
    try:
        with open("tpm_auth.json", "w") as f:
            json.dump(values, f, indent=2)
    except Exception as e:
        print(f"Error saving auth values: {e}")
