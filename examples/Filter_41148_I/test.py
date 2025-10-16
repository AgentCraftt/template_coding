from solution import binary_search

def test_binary_search_found():
    assert binary_search([1, 2, 3, 4, 5], 3) == 2
    assert binary_search([10, 20, 30, 40, 50], 10) == 0
    assert binary_search([10, 20, 30, 40, 50], 50) == 4

def test_binary_search_not_found():
    assert binary_search([1, 2, 3, 4, 5], 6) == -1
    assert binary_search([10, 20, 30, 40, 50], 25) == -1
    assert binary_search([], 1) == -1

def test_binary_search_single_element():
    assert binary_search([1], 1) == 0
    assert binary_search([2], 1) == -1

def test_binary_search_negative_numbers():
    assert binary_search([-5, -4, -3, -2, -1], -3) == 2
    assert binary_search([-5, -4, -3, -2, -1], 0) == -1
    assert binary_search([-5, -3, -1, 0, 1], -3) == 1