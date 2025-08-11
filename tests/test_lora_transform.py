from core.lora_transform import LoraTransform

def test_reinforce_settle():
    lt = LoraTransform()
    w = {}
    w = lt.reinforce(w, "joy", 0.9)
    w = lt.settle(w, "joy", 0.8)
    assert w["joy"] == 1.0
