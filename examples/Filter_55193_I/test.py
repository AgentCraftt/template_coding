from solution import bubble_sort


def test_bubble_sort_positive_numbers():
    assert bubble_sort([5, 3, 8, 4, 2]) == [2, 3, 4, 5, 8]


def test_bubble_sort_negative_numbers():
    assert bubble_sort([-4, -1, -7, -3, -9]) == [-9, -7, -4, -3, -1]


def test_bubble_sort_mixed_numbers():
    assert bubble_sort([3, -1, 4, -2, 0]) == [-2, -1, 0, 3, 4]


def test_bubble_sort_sorted_list():
    assert bubble_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_bubble_sort_reverse_sorted_list():
    assert bubble_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_bubble_sort_single_element():
    assert bubble_sort([5]) == [5]


def test_bubble_sort_empty_list():
    assert bubble_sort([]) == []
