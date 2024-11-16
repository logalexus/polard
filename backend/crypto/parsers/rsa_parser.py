from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from backend.crypto.parsers.parser import PublicKeyParser
from backend.logger import logger


class RSAParser(PublicKeyParser):
    def parse_key(self):
        parsers = [
            (serialization.load_ssh_public_key, "SSH"),
            (serialization.load_pem_public_key, "PEM"),
            (self._parse_certificate, "CERT")
        ]
        for parser, key_type in parsers:
            try:
                self.public_key = parser(self.key_data)
                self.type = key_type
                logger.info(f"{self.type} RSA key successfully loaded.")
                return
            except Exception:
                continue
        logger.error("Error parsing RSA key")

    def _parse_certificate(self, key_data):
        cert = load_pem_x509_certificate(key_data)
        return cert.public_key()

    def extract_parameters(self):
        if not self.public_key:
            logger.warning("No key loaded.")
            return None
        numbers = self.public_key.public_numbers()
        logger.info(f"Modulus (n): {numbers.n}")
        logger.info(f"Public exponent (e): {numbers.e}")
        return numbers


if __name__ == "__main__":
    keys = [
        "backend/crypto/examples/cert.crt",
        "backend/crypto/examples/id_rsa.pub",
        "backend/crypto/examples/pub.key"
    ]
    for key in keys:
        with open(key, "rb") as file:
            parser = RSAParser(file.read())
            parser.parse_key()
            numbers = parser.extract_parameters()
