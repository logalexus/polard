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
        # await asyncio.sleep(0) 
    if d == n:
        return None
    else:
        return d


def yafu_factor_driver(n):
    YAFU_BIN = "D:\\YandexDisk\\CodeCamp2022\\tools\\yafu-master\\yafu-x64.exe"
    # YAFU_BIN = "backend/crypto/bin/yafu/yafu-x64.exe"
    tmp = []
    proc = subprocess.Popen(
        [
            YAFU_BIN,
            f"factor({str(n)})",
            "-session",
            str(n),
            "-qssave",
            f"/tmp/qs_{str(n)}.dat",
        ],
        stdout=subprocess.PIPE,
    )
    for line in proc.stdout:
        line = line.rstrip().decode("utf8")
        if re.search(r"P\d+ = \d+", line):
            tmp += [int(line.split("=")[1])]
    return tmp
