import unittest
from core.slot import Slot, SlotPool

class TestSlot(unittest.TestCase):
    def test_decay(self):
        s = Slot(name="joy", angle_deg=0, value=0.1, decay=0.05)
        s.step_decay()
        self.assertAlmostEqual(s.value, 0.05)

    def test_pool_set_get(self):
        pool = SlotPool([Slot("joy", 0), Slot("anger", 270)])
        pool.set_value("joy", 0.8)
        self.assertEqual(pool.get("joy").value, 0.8)

if __name__ == "__main__":
    unittest.main()
