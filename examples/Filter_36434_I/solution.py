def count_distinct_elements(nums):
    """
    Returns the number of distinct elements in the list nums.
    The time complexity is O(n log n) due to sorting.
    """
    if not nums:
        return 0

    sorted_nums = sorted(nums)
    distinct_count = 1

    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] != sorted_nums[i - 1]:
            distinct_count += 1

    return distinct_count