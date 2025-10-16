def longest_common_prefix(words):
    """
    Finds the length of the longest common prefix in a list of words.
    
    :param words: List of uppercase strings of equal length
    :return: Length of the longest common prefix
    """
    if not words:
        return 0

    min_length = min(len(word) for word in words)
    prefix_length = 0

    for i in range(min_length):
        current_char = words[0][i]
        if all(word[i] == current_char for word in words):
            prefix_length += 1
        else:
            break

    return prefix_length