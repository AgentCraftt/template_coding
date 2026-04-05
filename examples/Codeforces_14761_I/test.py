from solution import minimal_distinct_deadlines


def test_example_1():
    n = 5
    deadlines = [1, 2, 2, 3, 5]
    assert minimal_distinct_deadlines(n, deadlines) == 5


def test_example_2():
    n = 4
    deadlines = [0, 0, 0, 0]
    assert minimal_distinct_deadlines(n, deadlines) == 4


def test_already_unique_deadlines():
    n = 4
    deadlines = [1, 2, 3, 4]
    assert minimal_distinct_deadlines(n, deadlines) == 4


def test_large_duplicates():
    n = 6
    deadlines = [10, 10, 10, 10, 10, 10]
    assert minimal_distinct_deadlines(n, deadlines) == 6


def test_mixed_small_and_large():
    n = 5
    deadlines = [0, 2, 4, 6, 6]
    assert minimal_distinct_deadlines(n, deadlines) == 5


def test_zero_and_negatives():
    n = 5
    deadlines = [0, 0, -1, -2, -3]
    assert minimal_distinct_deadlines(n, deadlines) == 5


def test_already_sequential():
    n = 5
    deadlines = [0, 1, 2, 3, 4]
    assert minimal_distinct_deadlines(n, deadlines) == 5
