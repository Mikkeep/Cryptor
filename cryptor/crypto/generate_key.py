from Crypto.PublicKey import RSA


class key_generator:
    def __init__(self) -> None:
        self.key = RSA.generate(2048)
        self.default_pub = "public.pem"
        self.default_priv = "private.pem"

    def generate_private_key(self, name=None):
        if name == None:
            name = self.default_priv
        private_key = self.key.export_key()
        file_out = open(name, "wb")
        file_out.write(private_key)
        file_out.close()

    def generate_public_key(self, name=None):
        if name == None:
            name = self.default_pub
        public_key = self.key.publickey().export_key()
        file_out = open(name, "wb")
        file_out.write(public_key)
