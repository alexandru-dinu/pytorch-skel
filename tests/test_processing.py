import unittest
import numpy as np

import bagoftools.processing as proc


class TestProcessing(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_splits(self):
        ns  = [1, 10, 32, 128, 137]
        bss = [1, 5, 8, 57, 64]
        for n in ns:
            for bs in [n, *bss]:
                xs = np.random.uniform(size=n)
                ys = proc.get_batches(xs, bs)
                self.assertEqual(len(ys), n//bs + (n % bs > 0))
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


if __name__ == '__main__':
    unittest.main()