from solution import count_distinct_elements

def test_no_elements():
    assert count_distinct_elements([]) == 0

def test_single_element():
    assert count_distinct_elements([1]) == 1

def test_all_distinct_elements():
    assert count_distinct_elements([1, 2, 3, 4, 5]) == 5

def test_all_same_elements():
    assert count_distinct_elements([2, 2, 2, 2, 2]) == 1

def test_mixed_elements():
    assert count_distinct_elements([1, 2, 2, 3, 3, 4, 5, 6, 6]) == 6

def test_elements_with_negatives():
    assert count_distinct_elements([-1, -1, 0, 1, 1, 2, 2]) == 4