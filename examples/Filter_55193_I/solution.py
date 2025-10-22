def bubble_sort(arr):
    """
    Performs bubble sort on a list of numbers.

    Parameters:
    arr (list of int/float): The list of numbers to be sorted.

    Returns:
    list of int/float: The sorted list of numbers.
    """
    n = len(arr)
    for i in range(n):
        # Track if a swap was made to optimize performance
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap if the element found is greater than the next element
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break
    return arr
