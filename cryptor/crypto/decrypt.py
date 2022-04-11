import os, random
from Crypto.Cipher import AES
import string
import os.path
from os import listdir
from os.path import isfile, join
from base64 import b64decode, b64encode
from Crypto import Random
from itertools import chain, product

class Encryptor():
    def __init__(self):
        self.block_size = AES.block_size
        self.iv = Random.new().read(self.block_size)
        print(self.iv)

    def __pad(self, plain_text):
        num_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_str = chr(num_bytes_to_pad)
        padding_str = num_bytes_to_pad * ascii_str
        if isinstance(plain_text, str):
            padded_txt = plain_text.decode('utf-8') + padding_str
            return padded_txt.encode()
        if isinstance(plain_text, bytes):       #checking for type was implemented for png file
            padded_txt = plain_text + padding_str.encode()
            return padded_txt
    
    def create_key(self):
        number = int(input("Insert number for ammount of randomness in key (0 - 16): "))
        ran = "".join(random.choices(string.ascii_lowercase + string.digits, k = number))
        key = "0"*(16-number)
        padded_key = ran + key
        print(padded_key)
        return padded_key

    def brute_key(self, charset, maxlength):
        return ("".join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(1, maxlength + 1)))


    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        #iv = Random.new().read(self.block_size)
        cipher = AES.new(self.create_key().encode('utf-8'), AES.MODE_CBC, self.iv)#.encode('utf-8'))
        encrypted_text = cipher.encrypt(plain_text)
        crypted = b64encode(self.iv + encrypted_text)
        return crypted

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as file:
            plaintext = file.read()
        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as file:
            file.write(enc)
            print("file encrypted")
            print("File named: " + file_name + ".enc")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        plain = self.decrypt(ciphertext)
        with open(file_name[:len(self.iv)] + ".decrypt", 'w') as fo:
            fo.write(plain)
            print("File decrypted!")
            print("Named: " + file_name + ".decrypt")

    def decrypt(self, encrypted_text):
        
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        print("Starting the bruteforcing, this might take some time")
        input()
        for attempt in self.brute_key(string.ascii_lowercase + string.digits, self.block_size):
            key = "0"*(16-len(attempt))
            padded_key = attempt + key
            print(padded_key)
            decryptor = AES.new(padded_key.encode('utf-8'), AES.MODE_CTR, iv)# self.iv_2)
            try:
                plaintext = decryptor.decrypt(encrypted_text[self.block_size:]).decode()
                print("found the key!")
                print(padded_key)
                return plaintext
            except UnicodeDecodeError:
                pass
        print("Couldn't find the used key for decryption. Exiting the program now")
        exit()

enc = Encryptor()
while True:
    choice = int(input(
        """Please choose option to either decrypt or encrypt: \n
        1. Decrypt a file
        2. Encrypt a file
        3. exit
        """))
    if choice == 1:
        enc.decrypt_file(str(input("Enter the name of the file you wish to decrypt: ")))
    
    elif choice == 2:
        enc.encrypt_file(str(input("Enter the name of the file you wish to encrypt: ")))
    
    elif choice == 3:
        exit()

    else:
        print("Please choose a valid option!!! ")
        #clear()