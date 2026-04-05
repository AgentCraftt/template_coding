from solution import longest_arith_seq_length


def test_example1():
    assert longest_arith_seq_length([3, 6, 9, 12]) == 4


def test_example2():
    assert longest_arith_seq_length([9, 4, 7, 2, 10]) == 3


def test_example3():
    assert longest_arith_seq_length([20, 1, 15, 3, 10, 5, 8]) == 4


def test_empty_list():
    assert longest_arith_seq_length([]) == 0


def test_single_element():
    assert longest_arith_seq_length([1]) == 1


def test_two_elements():
    assert longest_arith_seq_length([1, 3]) == 2


def test_no_arithmetic_subsequence():
    assert longest_arith_seq_length([1, 2, 4, 8, 16]) == 2


def test_large_common_difference():
    assert longest_arith_seq_length([10, 100, 1000, 10000]) == 2


def test_negative_numbers():
    assert longest_arith_seq_length([5, -5, -15, -25]) == 4
