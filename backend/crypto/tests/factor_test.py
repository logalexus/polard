from backend.crypto.methods.factor import yafu_factor_driver, pollard_rho
from Crypto.Util.number import getPrime

for i in range(10, 129):
    p = getPrime(i)
    q = getPrime(i)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0x10001
    d = pow(e, -1, phi)

    print(f"Bits = {i}")
    print(f"N = {n}")

    factor = yafu_factor_driver(n)
    p = factor
    q = n // p

    print(f"Factor: p = {p}, q = {q}")
    print()
