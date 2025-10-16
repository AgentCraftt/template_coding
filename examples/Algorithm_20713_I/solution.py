def flatten_list(nested_list):
    """
    Flattens a nested list of arbitrary depth into a single list of values.
    
    Args:
    nested_list (list): A list potentially nested to various depths.
    
    Returns:
    list: A flat list containing all elements from the nested structure.
    
    Raises:
    TypeError: If the input is not a list.
    """
    if not isinstance(nested_list, list):
        raise TypeError("Input must be a list")
    
    result = []
    for element in nested_list:
        if isinstance(element, list):
            result.extend(flatten_list(element))
        else:
            result.append(element)
    
    return result