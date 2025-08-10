from typing import Dict

class LoraTransform:
    """Pseudo LoRA-like transformation operations."""
    def reinforce(self, weights: Dict[str, float], slot: str, alpha: float = 0.1):
        weights[slot] = min(1.0, weights.get(slot, 0.0) + alpha)
        return weights

    def attenuate(self, weights: Dict[str, float], slot: str, beta: float = 0.1):
        weights[slot] = max(0.0, weights.get(slot, 0.0) - beta)
        return weights

    def blend(self, weights: Dict[str, float], a: str, b: str, ratio: float = 0.5):
        va, vb = weights.get(a, 0.0), weights.get(b, 0.0)
        m = (1 - ratio) * va + ratio * vb
        weights[a] = m
        weights[b] = m
        return weights

    def settle(self, weights: Dict[str, float], slot: str, threshold: float = 0.8):
        if weights.get(slot, 0.0) >= threshold:
            weights[slot] = 1.0
        return weights
