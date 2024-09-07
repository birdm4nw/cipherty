import time
import getpass
import signal
import sys
import os

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

from colorama import Fore, init
from io import BytesIO

from lib.db_operations import upload_file_to_db, get_file_from_db, get_all_files, delete_file_from_db

init()

errorMessage = f"\n{Fore.RED}[!]{Fore.RESET} Invalid option!"

def def_handler(sig, frame):
    print(f"\n\n{Fore.RED}[!]{Fore.RESET} Quitting..\n")
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

def heading():
    title = r"""
          _       _               _
      ___(_)_ __ | |__   ___ _ __| |_ _   _
     / __| | '_ \| '_ \ / _ \ '__| __| | | |
    | (__| | |_) | | | |  __/ |  | |_| |_| |
     \___|_| .__/|_| |_|\___|_|   \__|\__, |
           |_|                        |___/
    """
    author = f"\n\n{Fore.GREEN}[x] {Fore.RESET}Author: {Fore.GREEN}@{Fore.RESET}birdm4nw\n\n\n"
    print(f"{Fore.GREEN}{title}{Fore.RESET}")
    for letter in author:
        sys.stdout.write(letter)   
        sys.stdout.flush()        
        time.sleep(0.03)


def headers_animation(heading):
    line()
    for letter in heading:
        sys.stdout.write(Fore.GREEN + letter + Fore.RESET)   
        sys.stdout.flush()        
        time.sleep(0.08)  
    line()


def line():
    sys.stdout.write('\n' + '-' * 30 + '\n')   
    sys.stdout.flush()


def encrypt(password, inputFile):
    ext = os.path.splitext(inputFile)[1]

    with open(inputFile, 'rb') as file:
        dataFile = file.read()

    salt = get_random_bytes(16)
    # KDF (Key Derivation Function) to build a secure key and be able to cipher data in AES-256
    key = PBKDF2(password, salt, dkLen=32, count=1000000)

    # Cryptography mode that provides ENCRYPTION + AUTHENTICATION
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(dataFile)

    while True:
        pathToSave = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Enter a name for the encrpyted file: ")

        if not pathToSave:
            print(f"{Fore.RED}[!]{Fore.RESET} Filename can't be empty string!")
            continue
        else:
            outputFile = pathToSave + ext + ".enc"
            break

    try:
        with open(outputFile, 'wb') as file_out:
            file_out.write(salt + nonce + tag + ciphertext)
        
        print(f"\n{Fore.GREEN}[+]{Fore.RESET} Encrypted file successfully saved as {Fore.GREEN}{outputFile}{Fore.RESET}!")
        time.sleep(1)
        while True: 
            sel = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Would you like to export encrypted file to the database? (y/n): ")
            match sel:
                case "y":
                    description = input(f"\n{Fore.GREEN}[?]{Fore.RESET}  Enter a description for the encrypted file (e.g. Bank credentials): ")
                    print(f"\n{Fore.GREEN}[+]{Fore.RESET} Sending information to database..")
                    time.sleep(2)
                    upload_file_to_db(outputFile, description)
                    break
                case "n":
                    print(f"\n{Fore.GREEN}[+]{Fore.RESET} Your encrypted file will be stored in local")
                    break
                case _:
                    print(errorMessage)
            
    except ValueError:
        print(f"\n{Fore.RED}[!]{Fore.RESET} An error has occurred exporting the encrypted data!")
        sys.exit(1)
    time.sleep(2)
    
    while True:
        selForDeletion = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Would you like to delete the original file? (y/n): ")

        if selForDeletion == "y":
            shredding(inputFile)
            break
        elif selForDeletion == "n":
            break
        else:
            print(errorMessage)
            continue

    headers_animation("\tCLOSED_PROCESS")

def decrypt(password, encrypted_file=None, encrypted_data=None, ftype=None):
    ext = os.path.splitext(os.path.splitext(ftype)[0])[1]

    if encrypted_data:
        input_file = BytesIO(encrypted_data)
        salt = input_file.read(16)
        nonce = input_file.read(16)
        tag = input_file.read(16)
        ciphertext = input_file.read()

    elif encrypted_file:
        with open(encrypted_file, 'rb') as input_file:
            salt = input_file.read(16)
            nonce = input_file.read(16)
            tag = input_file.read(16)
            ciphertext = input_file.read()
    else:
        print(f"{Fore.RED}[!]{Fore.RESET} None file has been received!")

    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        decrypted_file = cipher.decrypt_and_verify(ciphertext, tag)
        filename = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Enter a name for the decrypted file: ")
        output_file = filename + ext

        with open(output_file, 'wb') as out_file:
            out_file.write(decrypted_file)

        print(f"\n{Fore.GREEN}[+]{Fore.RESET} File successfully decrypted!")

    except ValueError:
        print(errorMessage)

    headers_animation("\tCLOSED_PROCESS")

def file_exist(path):
    if os.path.isfile(file):
        return True
    else:
        print(f"{Fore.RED}[!]{Fore.RESET} File doesn't exist or is a directory")
        return False


def shredding(inputFile, passes=3):
    fsize = os.path.getsize(inputFile)

    with open (inputFile, "rb+") as f:
        for _ in range(passes):
            f.seek(0)
            f.write(os.urandom(fsize))
            f.flush()
            os.fsync(f.fileno())
        os.remove(inputFile)
        print(f"{Fore.RED}[!]{Fore.RESET} File {Fore.GREEN}{inputFile}{Fore.RESET} has been successfully deleted!")


if __name__ == '__main__':
    heading()    
    print(f"""
        {Fore.GREEN}[e]{Fore.RESET} Encrypt
        {Fore.GREEN}[d]{Fore.RESET} Decrypt
        {Fore.GREEN}[v]{Fore.RESET} View files stored in database
        {Fore.GREEN}[r]{Fore.RESET} Remove file from database
            """)
    act_1 = input(f"{Fore.GREEN}[+]{Fore.RESET} What action would you like to perform: ")
    time.sleep(1)
    os.system('clear')

    match act_1:
        case "e":
            headers_animation("\tFILE_ENCRYPTION")
            file = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Enter the path of the file to encrypt: ")
            if file_exist(file):
                while True:
                    passwd = getpass.getpass(prompt=f"\n{Fore.GREEN}[?]{Fore.RESET} Enter password: ")
                    if not passwd:
                        print(f"\n{Fore.RED}[!]{Fore.RESET} Password can't be empty string!")
                        continue
                    
                    passwd_conf = getpass.getpass(prompt=f"{Fore.GREEN}[?]{Fore.RESET}Confirm your password: ")

                    if passwd == passwd_conf:
                        print(f"\n{Fore.GREEN}[+]{Fore.RESET} Password configured correctly!")
                        break
                    else:
                        print(f"\n{Fore.RED}[!]{Fore.RESET} Passwords don't match! Try again!")

                encrypt(passwd, file)
        case "d":
            headers_animation("\tFILE_DECRYPTION")
            print(f"\n\t{Fore.GREEN}[l]{Fore.RESET} Local")
            print(f"\t{Fore.GREEN}[c]{Fore.RESET} Cloud")

            act_3 = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Where is stored the file to decrypt: ")
            match act_3:
                case "l":
                    file = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Enter the local path of the file to decrypt: ")
                    if file_exist(file):
                        passwd = getpass.getpass(f"\n{Fore.GREEN}[?]{Fore.RESET}Enter decryption password: ")
                        decrypt(passwd, encrypted_file=file, ftype=file)
                case "c":
                    binary_data, filename = get_file_from_db()
                    if binary_data:
                        passwd = getpass.getpass(f"\n{Fore.GREEN}[?]{Fore.RESET} Enter decryption password: ")
                        decrypt(passwd, encrypted_data=binary_data, ftype=filename)
                case _:
                    print(errorMessage)

        case "v":
            headers_animation("\tDATABASE_VIEW")
            get_all_files()
            headers_animation("\tCLOSED_PROCESS")
        case "r":
            headers_animation("\tFILE_DELETION")
            delete_file_from_db()
            headers_animation("\tCLOSED_PROCESS")
        case _:
            print(errorMessage)



