import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class BoldCryptor:
    def __init__(self, key: bytes, nonce: bytes):
        """Init of the bold cryptor."""
        self.key = key
        self.nonce = nonce
        self.counter = 0

    @staticmethod
    async def random(size: int) -> bytes:
        """Generate random bytes based on size."""
        return os.urandom(size)

    async def process(self, bytes_data: bytes) -> bytes:
        """Process the bytes and encrypt them."""
        iv = self.nonce + bytes([0, 0, self.counter])
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        self.counter += -(-len(bytes_data) // 16)  # Equivalent to Math.ceil(len(bytes_data) / 16)
        return encryptor.update(bytes_data) + encryptor.finalize()