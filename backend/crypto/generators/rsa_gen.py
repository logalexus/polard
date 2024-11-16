from Crypto.PublicKey.RSA import construct
from Crypto.Util.number import getPrime


def generate_pub_key(bits: 1024, format="PEM") -> str:
    if bits < 20 or bits > 4096:
        raise ValueError("Key size must be between 20 and 4096 bits")
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    n = p * q
    e = 0x10001
    key = construct((n, e))
    return key.publickey().export_key(format=format).decode('utf-8')