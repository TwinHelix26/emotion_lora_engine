import json, time, argparse
from pathlib import Path
from core.slot import Slot, SlotPool
from core.interference import interference_score
from core.lora_transform import LoraTransform
from core.memory_stack import MemoryStack
from core.state_monitor import StateMonitor

try:
    from ui.slot_visualizer import run as run_gui
except Exception:
    run_gui = None

PRESETS = Path(__file__).resolve().parents[1] / "data" / "presets" / "emotions_plutchik.json"

def load_presets():
    return json.loads(PRESETS.read_text(encoding="utf-8"))

def build_pool(preset):
    slots = [Slot(name=k, angle_deg=v, value=0.0) for k, v in preset.items()]
    return SlotPool(slots)

def main(gui=False):
    preset = load_presets()
    pool = build_pool(preset)
    lora = LoraTransform()
    mem = MemoryStack()
    monitor = StateMonitor()

    def apply_event(affect):
        for name, inc in affect.items():
            s = pool.get(name)
            for other in pool.slots.values():
                score = interference_score(s.angle_deg, other.angle_deg, hist=mem.summary_for(other.name))
                new_v = (inc + other.value * score) / (1.0 + score)
                pool.set_value(other.name, max(other.value, new_v))
            weights = {}
            weights = lora.reinforce(weights, name, alpha=min(0.2, inc))
            weights = lora.settle(weights, name, threshold=0.85)
            mem.push({"slot": name, "delta": inc})

    def values_dict():
        return {n: pool.get(n).value for n in pool.names()}

    if gui and run_gui:
        import threading, itertools
        def driver():
            seq = [
                {"joy": 0.5, "trust": 0.3},
                {"anger": 0.5},
                {"trust": 0.6},
                {"anticipation": 0.4},
            ]
            for ev in itertools.cycle(seq):
                apply_event(ev)
                time.sleep(0.4)
        threading.Thread(target=driver, daemon=True).start()
        run_gui(values_dict)
        return

    # CLI mode
    for step in range(10):
        if step in (0, 1, 6):
            apply_event({"joy": 0.6, "trust": 0.4})
        elif step in (2, 3):
            apply_event({"anger": 0.5})
        else:
            apply_event({"anticipation": 0.4})
        mode = monitor.estimate(values_dict())
        print(f"[step {step}] mode={mode} values={{k: round(v,2) for k,v in values_dict().items()}}")
        pool.tick()
        time.sleep(0.2)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gui", action="store_true", help="Show Tkinter GUI")
    args = ap.parse_args()
    main(gui=args.gui)
