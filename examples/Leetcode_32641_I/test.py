from solution import buildings_with_sunset_view

def test_example_case():
    assert buildings_with_sunset_view([4, 2, 3, 1]) == [0, 2, 3]

def test_all_buildings_can_see_sunset():
    assert buildings_with_sunset_view([1, 2, 3, 4]) == [3]

def test_no_building_can_see_sunset():
    assert buildings_with_sunset_view([4, 3, 2, 1]) == [0, 1, 2, 3]

def test_single_building():
    assert buildings_with_sunset_view([5]) == [0]

def test_all_buildings_of_same_height():
    assert buildings_with_sunset_view([4, 4, 4, 4]) == [3]

def test_random_heights():
    assert buildings_with_sunset_view([7, 3, 8, 3, 6, 1, 2]) == [2, 4, 6]