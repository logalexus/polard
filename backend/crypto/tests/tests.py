from abc import ABC, abstractmethod
from typing import List, Dict
from backend.crypto.factorizer import Factorizer
from backend.crypto.parsers.rsa_parser import RSAParser

class BaseTest(ABC):
    description: str

    @abstractmethod
    async def check(self, public_key: bytes, timeout: int = 30) -> bool:
        pass


class KeyLengthTest(BaseTest):
    description = "Key length >= 3072"

    async def check(self, public_key: bytes, timeout: int = 30) -> bool:
        parser = RSAParser(public_key)
        parser.parse_key()
        params = parser.extract_parameters()
        return params.n.bit_length() >= 3072


class PollardTest(BaseTest):
    description = "Factorization Pollard test"

    async def check(self, public_key: bytes, timeout: int = 30) -> bool:
        factorizer = Factorizer("Pollard")
        factorResult = await factorizer.factorize(public_key, timeout)
        return factorResult.status != "Success"


class YafuTest(BaseTest):
    description = "Factorization YAFU test"

    async def check(self, public_key: bytes, timeout: int = 30) -> bool:
        factorizer = Factorizer("Yafu")
        factorResult = await factorizer.factorize(public_key, timeout)
        return factorResult.status != "Success"
