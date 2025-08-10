import json, time
from pathlib import Path
from core.slot import Slot, SlotPool
from core.interference import interference_score
from core.memory_stack import MemoryStack

LOG = Path(__file__).resolve().parents[1] / "data" / "logs" / "example_interaction.json"
PRESETS = Path(__file__).resolve().parents[1] / "data" / "presets" / "emotions_plutchik.json"

def main():
    preset = json.loads(PRESETS.read_text(encoding="utf-8"))
    slots = [Slot(name=k, angle_deg=v, value=0.0) for k, v in preset.items()]
    pool = SlotPool(slots)
    mem = MemoryStack()

    events = json.loads(LOG.read_text(encoding="utf-8"))
    t_prev = 0
    for e in events:
        time.sleep(max(0, e["t"] - t_prev) * 0.2)
        for name, inc in e["affect"].items():
            s = pool.get(name)
            for other in pool.slots.values():
                score = interference_score(s.angle_deg, other.angle_deg, hist=mem.summary_for(other.name))
                new_v = (inc + other.value * score) / (1.0 + score)
                pool.set_value(other.name, max(other.value, new_v))
            mem.push({"slot": name, "delta": inc})
        print(f"[{e['t']}] {e['event']}: ", {n: round(pool.get(n).value,2) for n in pool.names()})
        pool.tick()
        t_prev = e["t"]

if __name__ == "__main__":
    main()
