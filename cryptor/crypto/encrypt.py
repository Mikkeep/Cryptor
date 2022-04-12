from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES, PKCS1_OAEP, ChaCha20_Poly1305
from Crypto.Random import get_random_bytes


class Encryption:
    # Init values are given to the class when called to generarate enc key
    def __init__(self, password="", algorithm=None, salt="", pwdLen=32):
        self.block_size = AES.block_size
        self.password = password
        self.algo = algorithm
        self.salt = salt
        self.pwdLen = pwdLen
        # PBKDF2 allows use of any length password provided by user
        self.enc_key = PBKDF2(self.password, self.salt, dkLen=self.pwdLen)

    def read_file(self, file_name):
        with open(file_name, "rb") as file:
            plaintext = file.read()
            return plaintext

    def encrypt_with_aes(self, filename):

        data = self.read_file(filename)

        cipher = AES.new(self.enc_key, AES.MODE_EAX)
        # MAC tag is used for authentication of the encrypted file/text
        ciphertext, tag = cipher.encrypt_and_digest(data)

        file_out = open("encrypted_" + filename, "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.close()
        print("File encrypted as " + "encrypted_" + filename)

    def encrypt_with_rsa(self, filename, pub_key=None):

        data = self.read_file(filename)

        if pub_key == None:
            from generate_key import key_generator

            generator = key_generator()
            generator.generate_public_key()
            generator.generate_private_key()
            print("Generated public and private key pair for RSA encryption")
            pub_key = generator.default_pub

        file_out = open("encrypted_" + filename, "wb")
        public_key = RSA.import_key(open(pub_key).read())
        # Session key generation, encrypts data symmetrically
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public key
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        [
            file_out.write(x)
            for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)
        ]
        file_out.close()

    def encrypt_with_chacha(self, filename):

        data = self.read_file(filename)

        cipher = ChaCha20_Poly1305.new(key=self.enc_key)

        ciphertext, tag = cipher.encrypt_and_digest(data)

        file_out = open("encrypted_" + filename, "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.close()
        print("File encrypted as " + "encrypted_" + filename)
