from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP, ChaCha20_Poly1305


class Decryption:
    # When class is called these values are given to it for key management
    def __init__(self, password="", algorithm=None, salt="", pwdLen=32):
        self.block_size = AES.block_size
        self.password = password
        self.algo = algorithm
        self.salt = salt
        self.pwdLen = pwdLen
        # PBKDF2 allows use of any length password provided by user
        self.dec_key = PBKDF2(self.password, self.salt, dkLen=pwdLen)

    def read_file(self, file_name):
        with open(file_name, "rb") as file:
            plaintext = file.read()
            return plaintext

    def write_file(self, file_name, data):
        with open(file_name, "w") as fo:
            fo.write(data)
            return data

    def open_file(self, filename):
        read_file = open(filename, "rb")
        return read_file

    def decrypt_with_aes(self, filename):

        try:
            file_in = open(filename, "rb")

            nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]

            cipher = AES.new(self.dec_key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)

            self.write_file(filename + ".dec", data.decode())

            return 0

        except (ValueError, KeyError):
            print("Failed decryption!")
            return -1

    def decrypt_with_rsa(self, filename, priv_key):

        try:
            file_in = self.open_file(filename)

            private_key = RSA.import_key(open(priv_key).read())

            enc_session_key, nonce, tag, ciphertext = [
                file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
            ]

            # Decrypt the session key with the private RSA key
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            # Decrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)

            self.write_file(filename + ".dec", data.decode())

            return 0

        except (ValueError, KeyError):
            print("Failed decryption!")
            return -1

    def decrypt_with_chacha(self, filename):

        try:
            file_in = open(filename, "rb")

            # Nonce is 12 bytes in default for ChaCha20_Poly1305
            nonce, tag, ciphertext = [file_in.read(x) for x in (12, 16, -1)]

            cipher = ChaCha20_Poly1305.new(key=self.dec_key, nonce=nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)

            self.write_file(filename + ".dec", data.decode())

            return 0

        except (ValueError, KeyError):
            print("Failed decryption!")
            return -1
