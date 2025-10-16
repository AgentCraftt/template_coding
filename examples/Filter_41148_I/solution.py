def binary_search(arr, target):
    """
    Performs binary search on a sorted array to find the target element.

    :param arr: List of sorted integers
    :param target: The integer to be searched
    :return: Index of the target element if found, else -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1