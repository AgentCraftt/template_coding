def test_find_subarrays_with_sum_basic():
    assert find_subarrays_with_sum([1, 1, 1], 2) == 2


def test_find_subarrays_with_sum_positive_and_negative():
    assert find_subarrays_with_sum([10, 2, -2, -20, 10], -10) == 3


def test_find_subarrays_with_sum_single_element_array():
    assert find_subarrays_with_sum([5], 5) == 1
    assert find_subarrays_with_sum([5], 0) == 0


def test_find_subarrays_with_sum_no_subarray():
    assert find_subarrays_with_sum([1, 2, 3], 6) == 1
    assert find_subarrays_with_sum([1, 2, 3], 7) == 0


def test_find_subarrays_with_sum_multiple_possible_subarrays():
    assert find_subarrays_with_sum([1, 2, 3, -2, 1, 4, 2], 5) == 4


def test_find_subarrays_with_sum_all_elements_same():
    assert find_subarrays_with_sum([2, 2, 2, 2], 4) == 3


def test_find_subarrays_with_sum_large_negative_target():
    assert find_subarrays_with_sum([-10, -10, -10], -20) == 2


def test_find_subarrays_with_sum_large_positive_target():
    assert find_subarrays_with_sum([10, 10, 10], 20) == 2
