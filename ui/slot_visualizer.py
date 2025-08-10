import tkinter as tk
from typing import Dict

class SlotVisualizer:
    def __init__(self, root, get_values_callable):
        self.root = root
        self.get_values = get_values_callable
        self.labels: Dict[str, tk.Label] = {}
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)
        self.root.title("emotion_lora_engine - Slot Visualizer")

    def _ensure_labels(self, names):
        for n in names:
            if n not in self.labels:
                lbl = tk.Label(self.frame, text=f"{n}: 0.00", anchor="w")
                lbl.pack(fill="x")
                self.labels[n] = lbl

    def tick(self):
        values = self.get_values()
        self._ensure_labels(values.keys())
        for n, v in values.items():
            self.labels[n]["text"] = f"{n}: {v:.2f}"
        self.root.after(200, self.tick)

def run(get_values_callable):
    root = tk.Tk()
    viz = SlotVisualizer(root, get_values_callable)
    viz.tick()
    root.mainloop()
