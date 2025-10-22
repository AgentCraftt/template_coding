from typing import Sequence
from collections import defaultdict


def find_subarrays_with_sum(arr: Sequence[int], target_sum: int) -> int:
    """
    Returns the number of contiguous subarrays that sum up to the target_sum.
    """
    count = 0
    current_sum = 0
    prefix_sum_count = defaultdict(int)
    prefix_sum_count[0] = 1  # For the subarray starting from the beginning

    for num in arr:
        current_sum += num
        if current_sum - target_sum in prefix_sum_count:
            count += prefix_sum_count[current_sum - target_sum]
        prefix_sum_count[current_sum] += 1

    return count
