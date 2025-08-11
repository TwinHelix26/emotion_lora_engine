from core.interference import interference_score

def test_interference_range():
    assert 0.0 <= interference_score(0, 0) <= 1.0
    assert 0.0 <= interference_score(0, 180) <= 1.0

def test_interference_symmetry():
    a = interference_score(10, 100)
    b = interference_score(100, 10)
    assert abs(a - b) < 1e-9
