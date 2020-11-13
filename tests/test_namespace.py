import json
import unittest

from bagoftools.namespace import Namespace


class TestNamespace(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_basic(self):
        d = Namespace()
        d.p1 = 2
        d.p2 = 3

        target = {'p1': 2, 'p2': 3}

        self.assertEqual(len(d), 2)
        self.assertDictEqual(d.to_dict(), target)
        self.assertEqual(str(d), json.dumps(target, indent=4))

    def test_nested(self):
        d = Namespace()
        d.l1 = 2
        d.l2 = Namespace()
        d.l2.p1 = 'a'
        d.l2.p2 = Namespace()
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

        d = Namespace()
        d.p1 = d
        d.p2 = C(x=3.14)
        d.p3 = self.__class__

        self.assertEqual(len(d), 3)
        self.assertDictEqual(d.to_dict(), {
            "p1": "<self>",
            "p2": "say hello to 3.14",
            "p3": "<class 'test_namespace.TestNamespace'>"
        })

    def test_recursive(self):
        x = {
            'p1': 1,
            'p2': {
                'x1': 2,
                'x2': {
                    'y1': [1, {'i': 'j'}],
                }
            }
        }

        d = Namespace(**x)
        self.assertEqual(len(d), 2)

        self.assertIsInstance(d.p2, Namespace)
        self.assertEqual(len(d.p2), 2)

        self.assertIsInstance(d.p2.x2, Namespace)
        self.assertEqual(len(d.p2.x2), 1)

        self.assertIsInstance(d.p2.x2.y1, list)
        self.assertIsInstance(d.p2.x2.y1[0], int)
        self.assertIsInstance(d.p2.x2.y1[1], Namespace)


if __name__ == '__main__':
    unittest.main()
