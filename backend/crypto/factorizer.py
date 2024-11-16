import asyncio
import time
from typing import Optional
from pydantic import BaseModel
from multiprocessing import Process, Queue
from backend.crypto.generators.rsa_gen import generate_pub_key
from backend.crypto.parsers.rsa_parser import RSAParser
from backend.crypto.methods.factor import pollard_rho, yafu_factor_driver
from Crypto.PublicKey.RSA import construct


class FactorResult(BaseModel):
    status: str
    private_key: Optional[str] = None
    factor_time: str


class Factorizer:
    def __init__(self, method: str = "Pollard"):
        self.method = method
        self.factor_func = self._get_method()

    def _get_method(self):
        methods = {
            "Pollard": pollard_rho,
            "Yafu": yafu_factor_driver
        }
        if self.method not in methods:
            raise ValueError("Invalid method")
        return methods[self.method]

    def _extract_parameters(self, public_key: bytes):
        parser = RSAParser(public_key)
        parser.parse_key()
        params = parser.extract_parameters()
        if not params:
            raise ValueError("Failed to extract RSA parameters")
        return params.n, params.e, parser.type

    def _calculate_private_key(self, n: int, e: int, p: int, key_type: str) -> str:
        q = n // p
        d = pow(e, -1, (p - 1) * (q - 1))
        private_key = construct((n, e, d)).export_key().decode()
        return private_key

    async def _factorization_worker(self, n: int):
        try:
            result = await asyncio.to_thread(self.factor_func, n)
            return result
        except Exception as e:
            return e

    async def factorize(self, public_key: bytes, timeout: int = 30) -> str:
        n, e, key_type = self._extract_parameters(public_key)

        start_time = time.time()
        try:
            result = await asyncio.wait_for(self._factorization_worker(n), timeout=timeout)
        except asyncio.TimeoutError:
            return FactorResult(status="Timeout", factor_time=str(timeout))
        
        elapsed_time = round(time.time() - start_time, 3)

        if isinstance(result, Exception):
            raise result

        p = result
        if not p or n % p != 0:
            raise ValueError("Failed to factorize modulus")

        private_key = self._calculate_private_key(n, e, p, key_type)
        return FactorResult(status="Success", private_key=private_key, factor_time=str(elapsed_time))


if __name__ == "__main__":
    key = generate_pub_key(100, "OpenSSH")
    print(key)
    factorizer = Factorizer(method="Pollard")
    res = factorizer.factorize(key.encode(), timeout=5)
    print(res)
