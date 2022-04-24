from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from base64 import b64encode


class salt_generator:
    """Generate salts for defaults"""
    def __init__(self) -> None:
        self.salt = ""
        # Number between 1 million and 9.9 million
        self.random = randint(1000000, 9999999)

    def generate_salt(self):
        """Creates random salt from bytes and B64 encodes it"""
        random_bytes = get_random_bytes(16)
        # Get 16 characters from the beginning
        self.salt = b64encode(random_bytes)[0:16]
        return self.salt.decode('utf-8')

    # Uses *args to accept arbitary amount of coords
    def generate_salt_from_coords(self, *coords):
        # Input coords are input with * to unpack coord tuples
        coord_val = 0
        coord_val = sum([coord for coord in coords])
        coord_val = coord_val * self.random
        return coord_val


# coord_tuple_1 = (600, 800)
# #print(*coord_tuple_1)
# coord_tuple_2 = (420, 69)

# salter = salt_generator()
# print(salter.generate_salt_from_coords(*coord_tuple_1, *coord_tuple_2))

# print(salter.generate_salt())