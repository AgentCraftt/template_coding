import pytest
from solution import flatten_list

def test_flatten_list_basic():
    assert flatten_list([1, 2, [3, 4], [5, [6, 7]]]) == [1, 2, 3, 4, 5, 6, 7]

def test_flatten_list_with_strings():
    assert flatten_list([['a', 'b'], ['c', ['d', ['e', 'f']]], 'g']) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']

def test_flatten_list_with_negative_numbers():
    assert flatten_list([-1, [-2, -3, [-4, -5], 0], 1]) == [-1, -2, -3, -4, -5, 0, 1]

def test_flatten_empty_list():
    assert flatten_list([]) == []

def test_flatten_nested_empty_lists():
    assert flatten_list([[[], [[]]]]) == []

def test_flatten_list_invalid_input_not_list():
    with pytest.raises(TypeError) as e:
        flatten_list("Not a list")
    assert str(e.value) == "Input must be a list"

def test_flatten_list_invalid_input_int():
    with pytest.raises(TypeError) as e:
        flatten_list(123)
    assert str(e.value) == "Input must be a list"

def test_flatten_list_invalid_input_dict():
    with pytest.raises(TypeError) as e:
        flatten_list({'key': 'value'})
    assert str(e.value) == "Input must be a list"