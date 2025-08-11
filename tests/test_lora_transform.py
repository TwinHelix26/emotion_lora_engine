import unittest
from core.lora_transform import LoraTransform

class TestLoraTransform(unittest.TestCase):
    def test_reinforce_settle(self):
        lt = LoraTransform()
        w = {}
        w = lt.reinforce(w, "joy", 0.9)
        w = lt.settle(w, "joy", 0.8)
        self.assertEqual(w["joy"], 1.0)

if __name__ == "__main__":
    unittest.main()
