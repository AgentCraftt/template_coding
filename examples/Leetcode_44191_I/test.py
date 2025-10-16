from solution import least_interval

def test_least_interval_with_example_case():
    assert least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 2) == 8
    
def test_least_interval_no_cooldown():
    assert least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 0) == 6

def test_least_interval_single_task():
    assert least_interval(['A'], 2) == 1
    
def test_least_interval_all_unique_tasks():
    assert least_interval(['A', 'B', 'C', 'D', 'E', 'F'], 2) == 6

def test_least_interval_with_multiple_task_repeats():
    assert least_interval(['A', 'A', 'A', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D'], 2) == 11

def test_least_interval_with_large_gap():
    assert least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 50) == 104