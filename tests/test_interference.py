import unittest
from core.interference import interference_score

class TestInterference(unittest.TestCase):
    def test_range(self):
        self.assertGreaterEqual(interference_score(0, 0), 0.0)
        self.assertLessEqual(interference_score(0, 180), 1.0)

    def test_symmetry(self):
        a = interference_score(10, 100)
        b = interference_score(100, 10)
        self.assertAlmostEqual(a, b, places=12)

if __name__ == "__main__":
    unittest.main()
