import json
import unittest

from bagoftools.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_basic(self):
        d = Config()
        d.p1 = 2
        d.p2 = 3

        target = {'p1': 2, 'p2': 3}

        self.assertEqual(len(d), 2)
        self.assertDictEqual(d.to_dict(), target)
        self.assertEqual(str(d), json.dumps(target, indent=4))

    def test_nested(self):
        d = Config()
        d.l1 = 2
        d.l2 = Config()
        d.l2.p1 = 'a'
        d.l2.p2 = Config()
        d.l2.p2.q1 = None

        target = {'l1': 2, 'l2': {'p1': 'a', 'p2': {'q1': None}}}

        self.assertEqual(len(d), 2)
        self.assertDictEqual(d.to_dict(), target)
        self.assertEqual(str(d), json.dumps(target, indent=4))

    def test_custom_params(self):
        class C:
            def __init__(self, x):
                self.x = x

            def __str__(self):
                return f'say hello to {self.x}'

        d = Config()
        d.p1 = d
        d.p2 = C(x=3.14)
        d.p3 = self.__class__

        self.assertEqual(len(d), 3)
        self.assertDictEqual(d.to_dict(), {
            "p1": "<self>",
            "p2": "say hello to 3.14",
            "p3": "<class 'test_config.TestConfig'>"
        })


if __name__ == '__main__':
    unittest.main()
