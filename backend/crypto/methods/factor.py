import asyncio
import re
import subprocess

from Crypto.Util.number import GCD

def pollard_rho(n, g=lambda x, n: (x**2 + 1) % n):
    n_length = len(str(n)) + 1
    x = 2
    y = 2
    d = 1
    while d == 1:
        x = g(x, n)
        y = g(g(y, n), n)
        d = GCD(abs(x-y), n)
    if d == n:
        return None
    else:
        return d


def yafu_factor_driver(n):
    YAFU_BIN = "backend/crypto/bin/yafu"
    tmp = []
    proc = subprocess.Popen(
        [
            YAFU_BIN,
            f"factor({str(n)})",
            f"-threads",
            f"10",
        ],
        stdout=subprocess.PIPE,
    )
    for line in proc.stdout:
        line = line.rstrip().decode("utf8")
        if re.search(r"P\d+ = \d+", line):
            tmp += [int(line.split("=")[1])]
    return tmp.pop()
