from typing import List, Dict

class MemoryStack:
    def __init__(self):
        self.events: List[Dict] = []

    def push(self, event: Dict):
        self.events.append(event)

    def summary_for(self, slot: str, last_n: int = 50) -> float:
        rel = [e.get("delta", 0.0) for e in self.events[-last_n:] if e.get("slot") == slot]
        if not rel:
            return 0.0
        s = sum(rel)
        return max(-1.0, min(1.0, s / max(1, len(rel))))
