import json
import unittest

from bagoftools.imports import *


class TestImports(unittest.TestCase):
    def setUp(self) -> None:
        self.modules = [
            'os', 'sys', 'time', 'math',
            're', 'reduce', 'operator', 'itertools',
            'np', 'sns', 'plt',
            'pickle', 'tqdm', 'pprint'
        ]

    def tearDown(self) -> None:
        pass

    def test_basic(self):
        g = globals().keys()
        for m in self.modules:
            self.assertIn(m, g)


if __name__ == '__main__':
    unittest.main()
