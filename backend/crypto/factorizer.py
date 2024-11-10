import time
from backend.crypto.parsers.rsa_parser import RSAParser
from backend.crypto.methods.factor import pollard_rho, yafu_factor_driver
from Crypto.PublicKey.RSA import construct



class Factorizer():
    def __init__(self, public_key: bytes) -> None:
        self.public_key = public_key

    def get_method(self, method: str = "Pollard"):
        if method == "Pollard":
            return pollard_rho
        elif method == "Yafu":
            return yafu_factor_driver
        else:
            raise ValueError("Invalid method")

    def factorize(self, method: str = "Pollard") -> str:
        try:
            parser = RSAParser(self.public_key)
            parser.parse_key()
            params = parser.extract_parameters()
            n = params.n
            e = params.e
            factor_func = self.get_method(method)

            start_time = time.time()
            p = factor_func(n)
            end_time = time.time()

            elapsed_time = round(float(end_time - start_time), 3)

            q = n // p
            d = pow(e, -1, (p - 1) * (q - 1))

            private_key = construct((n, e, d)).export_key().decode()

            return private_key, str(elapsed_time)
        except:
            pass
