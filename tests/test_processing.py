import unittest

import numpy as np

import bagoftools.processing as proc


class TestProcessing(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_splits(self):
        ns = [10, 32, 59]
        for n in ns:
            for bs in np.arange(1, n + 1):
                xs = np.random.uniform(size=n)
                ys = proc.get_batches(xs, int(bs))
                self.assertEqual(len(ys), n // bs + (n % bs > 0))
                for y in ys[:-1]:
                    self.assertEqual(len(y), bs)
                r = bs if n % bs == 0 else n % bs
                self.assertEqual(len(ys[-1]), r)

    def test_reconstruct(self):
        n = np.random.randint(100, 200)
        bs = np.random.randint(1, 32)
        xs = np.random.uniform(size=n)
        ys = proc.get_batches(xs, bs)
        zs = np.array([x for y in ys for x in y])
        self.assertTrue(np.isclose(xs, zs).all())

    def test_with_other_types(self):
        for _type in [list, tuple]:
            xs = _type(range(100))
            bs = 25
            ys = proc.get_batches(xs, bs)
            self.assertEqual(len(ys), 4)
            for y in ys:
                self.assertEqual(len(y), bs)

    def test_with_wrong_batch_size(self):
        xs = np.random.uniform(size=100)
        for bs in [-10, 0, 10000, -0.12, 7.123]:
            with self.assertRaises(ValueError):
                _ = proc.get_batches(xs, bs)

    def test_map_function(self):
        xs = [1.1, -0.25, 3]
        ys = proc.map_batchwise(xs, bs=3, func=lambda x: np.round(abs(x)))
        self.assertTrue((ys[0] == [1, 0, 3]).all())


if __name__ == '__main__':
    unittest.main()
