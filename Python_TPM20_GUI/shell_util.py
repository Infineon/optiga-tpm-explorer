import subprocess
import os
from subprocess import PIPE

# Variables to hold the 3 authorisation values
ownerAuth = "owner123"
nvAuth = "nv123"
endorseAuth = "endorsement123"
lockoutAuth = "lockout123"
openssl_cnf=("openssl_conf = openssl_init\n"
            "[openssl_init]\n"
            "engines = engine_section\n"
            "[engine_section]\n"
            "tpm2tss = tpm2tss_section\n"
            "[tpm2tss_section]\n"
            "engine_id = tpm2tss\n"
            #~ "dynamic_path = /usr/lib/arm-linux-gnueabihf/engines-1.1/libtpm2tss.so\n"
            "default_algorithms = ALL\n"
            "init = 1\n"
            "SET_OWNERAUTH = %s\n" 
            "[req]\n"
            "distinguished_name = subject\n"
            "[subject]\n" % ownerAuth)


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
    if (diff_length > 0):
        while (diff_length > 0):
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
    return(output.decode())


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
    return(output.decode())


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
    return(output.decode())


def createProcess(cmd, file):
    output = ""
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)
        
    return(output)


def createProcess_PIPE(cmd, file):
    output = ""
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)
    return(output)
