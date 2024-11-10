from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from backend.crypto.parsers.parser import PublicKeyParser
from backend.logger import logger

class RSAParser(PublicKeyParser):
    def parse_key(self):
        try:
            if self.key_data.startswith(b'ssh-rsa'):
                self.public_key = serialization.load_ssh_public_key(self.key_data)
            else:
                self.public_key = serialization.load_pem_public_key(self.key_data) \
                                  if self.key_data.startswith(b'-----BEGIN PUBLIC KEY-----') \
                                  else serialization.load_der_public_key(self.key_data)

            if not isinstance(self.public_key, rsa.RSAPublicKey):
                raise ValueError("This is not an RSA key")
            logger.info("RSA key successfully loaded.")
        except Exception as e:
            logger.error(f"Error parsing RSA key: {e}")

    def get_key_type(self):
        if isinstance(self.public_key, rsa.RSAPublicKey):
            return "RSA"
        return None

    def extract_parameters(self):
        if self.public_key:
            numbers = self.public_key.public_numbers()
            logger.info(f"Modulus (n): {numbers.n}")
            logger.info(f"Public exponent (e): {numbers.e}")
            return numbers
        else:
            logger.warning("No key loaded.")
