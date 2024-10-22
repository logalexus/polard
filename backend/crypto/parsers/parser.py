from abc import ABC, abstractmethod


class PublicKeyParser(ABC):
    def __init__(self, key_data: bytes):
        self.key_data = key_data
        self.public_key = None

    @abstractmethod
    def parse_key(self):
        pass

    @abstractmethod
    def get_key_type(self):
        pass

    @abstractmethod
    def extract_parameters(self):
        pass
