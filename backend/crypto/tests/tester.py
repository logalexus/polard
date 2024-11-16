from typing import Dict, List
from backend.crypto.tests.tests import BaseTest, KeyLengthTest, PollardTest, YafuTest


class PublicKeyTester:
    def __init__(self):
        self.tests: List[BaseTest] = [
            KeyLengthTest(),
            PollardTest(),
            YafuTest()
        ]

    async def run_tests(self, public_key: str, timeout: int = 30) -> List[Dict[str, str]]:
        results = []
        for test in self.tests:
            result = await test.check(public_key, timeout)
            results.append({
                "description": test.description,
                "status": result
            })
        return results
