from solution import create_symmetric_matrix
import numpy as np


def test_create_symmetric_matrix_valid_input():
    vector = [1, 2, 3, 4, 5, 6]
    expected_matrix = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
    result = create_symmetric_matrix(vector)
    assert np.array_equal(result, expected_matrix)


def test_create_symmetric_matrix_single_element():
    vector = [1]
    expected_matrix = np.array([[1]])
    result = create_symmetric_matrix(vector)
    assert np.array_equal(result, expected_matrix)


def test_create_symmetric_matrix_invalid_length():
    vector = [1, 2, 3, 4]
    try:
        create_symmetric_matrix(vector)
        assert False, "Expected ValueError for invalid input length"
    except ValueError:
        pass


def test_create_symmetric_matrix_larger_valid_input():
    vector = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected_matrix = np.array(
        [[1, 2, 3, 4], [2, 5, 6, 7], [3, 6, 8, 9], [4, 7, 9, 10]]
    )
    result = create_symmetric_matrix(vector)
    assert np.array_equal(result, expected_matrix)
