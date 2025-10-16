from solution import min_distance_pair

def test_min_distance_pair_simple():
    arr1 = [1, 2, 3]
    arr2 = [1, 2, 3]
    result = min_distance_pair(arr1, arr2)
    assert result in [[0, 1], [1, 2]]

def test_min_distance_pair_tie():
    arr1 = [1, 1, 4, 4]
    arr2 = [1, 2, 1, 2]
    result = min_distance_pair(arr1, arr2)
    assert result in [[0, 1], [2, 3], [0, 2], [1, 3]]

def test_min_distance_pair_negative():
    arr1 = [-1, -2, -3]
    arr2 = [-1, -3, -2]
    result = min_distance_pair(arr1, arr2)
    assert result == [0, 1] or result == [1, 2]

def test_min_distance_pair_mixed():
    arr1 = [1, -3, 4]
    arr2 = [-2, 3, -1]
    result = min_distance_pair(arr1, arr2)
    assert result == [0, 2]

def test_min_distance_pair_large():
    arr1 = [i for i in range(10)]
    arr2 = [i for i in range(10)]
    result = min_distance_pair(arr1, arr2)
    assert result in [[i, i + 1] for i in range(9)]