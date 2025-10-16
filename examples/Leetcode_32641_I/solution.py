def buildings_with_sunset_view(heights):
    """
    Returns the list of indices of buildings that can see the sunset.
    A building can see the sunset if all the buildings to its right are shorter.
    """
    result = []
    current_max_height = 0
    for i in range(len(heights) - 1, -1, -1):
        if heights[i] > current_max_height:
            result.append(i)
            current_max_height = heights[i]
    result.reverse()
    return result