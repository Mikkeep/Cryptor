from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256, SHA512, SHA3_512, MD5
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

    def encrypt_with_aes(self, filename, fileout):

        data = self.read_file(filename)

        mode = AES.new(self.enc_key, AES.MODE_EAX)
        # MAC tag is used for authentication of the encrypted file/text
        encrypt_text, tag = mode.encrypt_and_digest(data)

        file_out = open("encrypted_" + fileout, "wb")
        [file_out.write(x) for x in (mode.nonce, tag, encrypt_text)]
        file_out.close()
        print("File encrypted as " + "encrypted_" + fileout)

    def encrypt_with_rsa(self, filename, fileout, pub_key=None):

        data = self.read_file(filename)

        if pub_key == None:

            try:
                # Read both for confirmation they exist
                self.read_file("public.pem")
                self.read_file("private.pem")
                print("Found existing RSA key pair")
                pub_key = "public.pem"

            # If not found handle the error by generating new AES key pair
            except FileNotFoundError:

                print("Existing RSA key pair not found")

                from .generate_key import key_generator

                generator = key_generator()
                generator.generate_public_key()
                generator.generate_private_key()
                print("Generated public and private key pair for RSA encryption")
                pub_key = generator.default_pub

        file_out = open("encrypted_" + fileout, "wb")
        public_key = RSA.import_key(open(pub_key).read())
        # Session key generation, encrypts data symmetrically
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public key
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        secret_text, tag = cipher_aes.encrypt_and_digest(data)
        [
            file_out.write(x)
            for x in (enc_session_key, cipher_aes.nonce, tag, secret_text)
        ]
        file_out.close()
        print("File encrypted as " + "encrypted_" + fileout)

    def encrypt_with_chacha(self, filename, fileout):

        data = self.read_file(filename)

        # Used key must be 32 bytes long
        cipher = ChaCha20_Poly1305.new(key=self.enc_key)

        secret, tag = cipher.encrypt_and_digest(data)

        file_out = open("encrypted_" + fileout, "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, secret)]
        file_out.close()
        print("File encrypted as " + "encrypted_" + fileout)

    def hash_with_sha256(self, plaintext):

        hash = SHA256.new()
        if self.salt != "":
            plaintext = self.salt + plaintext
        hash.update(plaintext.encode("utf-8"))
        return hash.hexdigest()

    def hash_with_sha512(self, plaintext):

        hash = SHA512.new()
        if self.salt != "":
            plaintext = self.salt + plaintext
        hash.update(plaintext.encode("utf-8"))
        return hash.hexdigest()

    def hash_with_sha3_512(self, plaintext):

        hash = SHA3_512.new()
        if self.salt != "":
            plaintext = self.salt + plaintext
        hash.update(plaintext.encode("utf-8"))
        return hash.hexdigest()

    def hash_with_md5(self, plaintext):

        hash = MD5.new()
        if self.salt != "":
            plaintext = self.salt + plaintext
        hash.update(plaintext.encode("utf-8"))
        return hash.hexdigest()
