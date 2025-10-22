def longest_arith_seq_length(nums):
    """
    Find the length of the longest arithmetic subsequence in the given list of integers.

    :param nums: List[int] - a list of integers
    :return: int - the length of the longest arithmetic subsequence
    """
    if not nums:
        return 0

    # Dictionary to store the length of the longest arithmetic sequence ending with nums[i]
    # and having a common difference of `d`.
    dp = [{} for _ in range(len(nums))]
    max_len = 1

    for i in range(len(nums)):
        for j in range(i):
            diff = nums[i] - nums[j]
            # If the same difference has been seen for the subsequences ending at index j,
            # extend that subsequence. Otherwise, start a new subsequence.
            if diff in dp[j]:
                dp[i][diff] = dp[j][diff] + 1
            else:
                dp[i][diff] = (
                    2  # Starting a new subsequence with at least 2 elements (nums[j] and nums[i])
                )
            max_len = max(max_len, dp[i][diff])

    return max_len
