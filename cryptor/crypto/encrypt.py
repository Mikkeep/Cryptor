import tarfile
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
from Crypto.Protocol.KDF import PBKDF2


class Encryption:
    def __init__(self, key=None, algorithm=None, salt=""):
        self.block_size = AES.block_size
        self.key = key
        self.algo = algorithm
        self.salt = salt
        print(self.key, self.algo, self.salt)
        self.enc_key = PBKDF2(self.key, self.salt, dkLen=32)
        print("self.enc_key: ", self.enc_key)

    def encrypt(self, plain_text):
        cipher = AES.new(self.enc_key, AES.MODE_CTR)
        encrypted_text = cipher.encrypt(plain_text)
        crypted = b64encode(encrypted_text)
        return crypted

    def decrypt(self, ciphertext):
        ciphertext = b64decode(ciphertext)
        cipher = AES.new(self.enc_key, AES.MODE_CTR)
        cleartext = cipher.decrypt(ciphertext)
        decrypted = b64decode(cleartext)
        return decrypted

    def encrypt_file(self, file_name):
        with open(file_name, "rb") as file:
            plaintext = file.read()
        enc = self.encrypt(plaintext)
        with open("encrypted_" + file_name, "wb") as file:
            file.write(enc)
            print("file encrypted")
            print("File named: " + file_name + ".enc")

    def decrypt_file(self, file_name):
        with open(file_name, "rb") as file:
            ciphertext = file.read()
        dec = self.decrypt(ciphertext)
        with open("decrypted_" + file_name, "wb") as file:
            file.write(dec)
            print("File decrypted")
            print("File named: " + file_name + ".dec")


class Compression:
    def compress(self, tar_file, filelist):
        # open file for gzip compression
        tar = tarfile.open(tar_file, mode="w:gz")
        print(file_list)
        for file in filelist:
            tar.add(file)
        tar.close()

    def decompress(self, tar_file, path, members=None):
        tar = tarfile.open(tar_file, mode="r:gz")
        if members is None:
            members = tar.getmembers()
            print(members)
        for member in members:
            tar.extract(member, path=path)
        tar.close()


# secret = Secrects()
secret_1 = Encryption("avain", "algoritmi", "suola")
input()
# secret.encrypt_file(str(input("Please input a file to encrypt: ")))
# secret.decrypt_file(str(input("Please input a file to encrypt: ")))
file = input("Give file plez: ")
file_list = []
file_list.append(file)
compresser = Compression()
compresser.compress("tartest_PDF", file_list)
secret_1.encrypt_file(str(input("Please input a file to encrypt: ")))
input("File is now ecnrypted, press Enter")
secret_1.decrypt(str(input("Please input a file to decrypt: ")))
compresser.decompress("decrypted_tartest_PDF", "test_deflate/new_folder/")
# secret.encrypt_file(str(input("Please input a file to encrypt: ")))
# secret.decrypt_file(str(input("Please input a file to decrypt: ")))
# decompress("tartest_PDF", "test_deflate/new_folder/")
