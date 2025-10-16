def min_distance_pair(arr1, arr2):
    """
    Finds the pair of distinct points such that the distance between them is minimized.
    Returns the indices of these two points as a list [i, j] with i < j.
    """
    n = len(arr1)
    min_distance = float('inf')
    min_pair = None
    for i in range(n):
        for j in range(i + 1, n):
            distance = abs(arr1[i] - arr1[j]) + abs(arr2[i] - arr2[j])
            if distance < min_distance:
                min_distance = distance
                min_pair = [i, j]
    return min_pair