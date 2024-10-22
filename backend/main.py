from backend.crypto.parsers.rsa_parser import RSAParser
from backend.crypto.parsers.ecdsa_parser import ECDSAParser
from fastapi import FastAPI

def main():
    with open("backend/crypto/examples/id_rsa.pub", "rb") as file:
        key = file.read()
    
    key = RSAParser(key)
    key.parse_key()
    key.extract_parameters()
    
    with open("backend/crypto/examples/id_ecdsa.pub", "rb") as file:
        key = file.read()
    
    key = ECDSAParser(key)
    key.parse_key()
    key.extract_parameters()
    
    

if __name__ == "__main__":
    main()
