import math
from typing import Tuple

def _angle_diff(a: float, b: float) -> float:
    d = abs((a - b + 180) % 360 - 180)
    return d  # 0..180

def interference_score(angle_a: float, angle_b: float, w_hist: float = 0.2, hist: float = 0.0) -> float:
    """Phase-based interference: 1.0=best (in-phase), 0.0=worst (opposite)."""
    base = 1.0 - (_angle_diff(angle_a, angle_b) / 180.0)
    return max(0.0, min(1.0, (1 - w_hist) * base + w_hist * ((hist + 1) / 2)))

def mix_intensity(v_a: float, v_b: float, score: float) -> float:
    """Weighted mix by interference score (0..1)."""
    return max(0.0, min(1.0, (v_a + v_b * score) / (1.0 + score)))

def compound_emotion(angle_a: float, angle_b: float, v_a: float, v_b: float) -> Tuple[float, float]:
    """Return compound angle and intensity via vector sum."""
    ax = math.cos(math.radians(angle_a)) * v_a
    ay = math.sin(math.radians(angle_a)) * v_a
    bx = math.cos(math.radians(angle_b)) * v_b
    by = math.sin(math.radians(angle_b)) * v_b
    x, y = ax + bx, ay + by
    if x == 0 and y == 0:
        angle = angle_a
    else:
        angle = (math.degrees(math.atan2(y, x)) + 360) % 360
    value = max(0.0, min(1.0, math.sqrt(x*x + y*y)))
    return angle, value
