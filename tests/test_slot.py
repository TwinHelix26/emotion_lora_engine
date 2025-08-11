from core.slot import Slot, SlotPool

def test_decay():
    s = Slot(name="joy", angle_deg=0, value=0.1, decay=0.05)
    s.step_decay()
    assert abs(s.value - 0.05) < 1e-9

def test_pool_set_get():
    pool = SlotPool([Slot("joy", 0), Slot("anger", 270)])
    pool.set_value("joy", 0.8)
    assert pool.get("joy").value == 0.8
