from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Slot:
    name: str
    angle_deg: float
    value: float = 0.0
    decay: float = 0.01
    bias: float = 0.0
    metadata: Dict = field(default_factory=dict)

    def step_decay(self):
        self.value = max(0.0, self.value - self.decay)

class SlotPool:
    def __init__(self, slots: List['Slot']):
        self.slots: Dict[str, Slot] = {s.name: s for s in slots}

    def get(self, name: str) -> Slot:
        return self.slots[name]

    def names(self) -> List[str]:
        return list(self.slots.keys())

    def values(self) -> Dict[str, float]:
        return {n: s.value for n, s in self.slots.items()}

    def tick(self):
        for s in self.slots.values():
            s.step_decay()

    def set_value(self, name: str, v: float):
        self.slots[name].value = max(0.0, min(1.0, v))
