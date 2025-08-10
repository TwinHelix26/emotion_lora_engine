from typing import Dict

class StateMonitor:
    def estimate(self, slot_values: Dict[str, float]) -> str:
        v = list(slot_values.values())
        if not v:
            return "idle"
        avg = sum(v) / len(v)
        peak = max(v)
        if peak > 0.8 and avg < 0.4:
            return "focused"
        if avg > 0.6:
            return "overloaded"
        if avg < 0.1:
            return "calm"
        return "normal"
