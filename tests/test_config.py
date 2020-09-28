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


if __name__ == '__main__':
    unittest.main()