from solution import array_to_string

def test_array_to_string_single_element():
    assert array_to_string([1]) == '1'

def test_array_to_string_multiple_elements():
    assert array_to_string([1, 2, 3, 4, 5]) == '1,2,3,4,5'

def test_array_to_string_including_negative_numbers():
    assert array_to_string([-1, -2, 3, 4, -5]) == '-1,-2,3,4,-5'

def test_array_to_string_with_zero():
    assert array_to_string([0, 1, 2]) == '0,1,2'

def test_array_to_string_empty_array():
    assert array_to_string([]) == ''