import cryptography
from cryptography.fernet import Fernet
import os
import sys
import binascii

# Generate the key and put it in a file
def generate_write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
        key_file.close()

# Bring the key from the file
def load_key():
    return open("key.key", "rb").read()


# Ecrypt file with the key
def encrypt(file, fernet):
    with open(file, "rb") as el:
        data = el.read()
    with open(file, "wb") as elw:
        enc = fernet.encrypt(data)
        elw.write(enc)

# Decrypt file with the key
def decrypt(file, fernet):
    with open(file, "rb") as dl:
        data = dl.read()
    with open(file, "wb") as dlw:
        dec = fernet.decrypt(data)
        dlw.write(dec)

# Encrypt directory with the key
def encrypt_dir(file, fernet):
    for files in os.listdir(file):
        if os.path.isfile(str(file + files)) == True:
            print("Encrypting file", files)
            encrypt(str(file + files), fernet)
        elif os.path.isdir(str(file + files)) == True:
            print("Encrypting directory", files)
            encrypt_dir(str(file + files + "/"), fernet)

# Decrypt directory with the key
def decrypt_dir(file, fernet):
    for files in os.listdir(file):
        if os.path.isfile(str(file + files)) == True:
            print("Decrypting file", files)
            decrypt(str(file + files), fernet)
        elif os.path.isdir(str(file + files)) == True:
            print("Decrypting directory", files)
            decrypt_dir(str(file + files + "/"), fernet)

# main
if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Welcome to Crypter!")
        print("\nThis python programm can encrypt and decrypt file or directory, so use it carefully.")
        print("\nCOMMAND:")
        print("python3 crypter.py FILE_OR_DIRECTORY_NAME")
        print("\nOPTIONS:")
        print("    -e [to encrypt file]\n    -d [to decrypt file]\n    -ed [to encrypt directory]\n    -dd [to decrypt directory]")
        print("\nThe KEY will be saved on the file 'key.key'!")
        print("\nMade by Nicola Travaglini")
        quit()

    # Verify the key and bring that, or generate it and bring it
    if os.path.isfile("key.key") == True:
        if os.stat("key.key").st_size == 0:
            generate_write_key()
        k = load_key()
    else:
        generate_write_key()
        k = load_key()
    
    print("Key generated or verificated.")
    # k = KEY, so print it
    print("KEY:", k.decode("utf-8"))

    # Initialize the Fernet
    try:
        f = Fernet(k)
    except binascii.Error:
        print("You can't modify with words the file 'key.key'!")
        quit()

    try:
        # Select the file
        file = sys.argv[1]
        # Select your choose
        choose = sys.argv[2]
    except IndexError:
        print("You have to put both COMMAND and a OPTION!")
        quit()

    # Verify the file / directory
    if os.path.isfile(file) == True:
        print("File verificated.")
    else:
        if choose == "-ed" or choose == "-dd":
            if os.path.exists(file):
                print("Directory verificated.")
            else:
                print("Directory", file, "doesn't exist!")
                quit()
        else:
            print("File", file, "doesn't exist!")
            quit()

    # Verify choose and attack
    if choose == "-e":
        print("Encrypting file", file)
        encrypt(file, f)
    
    elif choose == "-d":
        print("Decrypting file", file)
        try:
            decrypt(file, f)
        except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken):
            print("The KEY has been changed, your file is lost.")
            quit()

    elif choose == "-ed":
        print("Encrypting directory", file)
        encrypt_dir(file, f)
            
    elif choose == "-dd":
        print("Decrypting directory", file)
        try:
            decrypt_dir(file, f)
        except cryptography.fernet.InvalidToken:
            print("This directory isn't yet encrypted!")
            quit()

    else:
        print("Options", choose, "isn't valid!")
        quit()
    
    # print the final message DONE!
    print("DONE!")