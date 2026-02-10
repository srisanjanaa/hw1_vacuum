from vacuum_world import VacuumWorld

def test_successors_clean():
    grid = [
        "S",
        "D",
    ]
    p = VacuumWorld.from_grid(grid)
    s0 = p.initial_state()
    succ = list(p.successors(s0))
    # From (0,0): can move DOWN, cannot CLEAN (not dirty)
    acts = set(a for a, _, _ in succ)
    assert "DOWN" in acts
    assert "CLEAN" not in acts

def test_clean_action():
    grid = [
        "S",
        "D",
    ]
    p = VacuumWorld.from_grid(grid)
    # move down then clean
    s0 = p.initial_state()
    down_state = [ns for a, ns, _ in p.successors(s0) if a == "DOWN"][0]
    succ2 = list(p.successors(down_state))
    acts2 = set(a for a, _, _ in succ2)
    assert "CLEAN" in acts2

def run_all():
    test_successors_clean()
    test_clean_action()
    print("All tests passed!")

if __name__ == "__main__":
    run_all()
