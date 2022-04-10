import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

class Secrects():

    def __init__(self):
        self.block_size = AES.block_size
        self.key = "12345mikke123456"
    """
    def __pad(self, plain_text):
        num_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_str = chr(num_bytes_to_pad)
        padding_str = num_bytes_to_pad * ascii_str
        padded_txt = plain_text.decode('utf-8') + padding_str
        return padded_txt.encode()
    """

    def encrypt(self, plain_text):
        plain_text = pad(plain_text, self.block_size)
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CTR) # <-- change this for different modes
        encrypted_text = cipher.encrypt(plain_text)              #ECB, CBC, CTR for this assignment
        print("Length of the encyption is -> " + str(len(encrypted_text)))
        crypted = b64encode(encrypted_text)
#        print(crypted)
        return crypted

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as file:
            plaintext = file.read()
        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as file:
            file.write(enc)
            print("file encrypted")
            print("File named: " + file_name + ".enc")

    #TODO:
    #Add decrypt for this encryption


secret = Secrects()
secret.encrypt_file(str(input("Please input a file to encrypt: ")))