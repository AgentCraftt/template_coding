def test_calculateTrappedWater():
    assert calculateTrappedWater([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert calculateTrappedWater([4, 2, 0, 3, 2, 5]) == 9
    assert calculateTrappedWater([]) == 0
    assert calculateTrappedWater([1, 2, 1]) == 0
    assert calculateTrappedWater([2, 0, 2]) == 2
    assert calculateTrappedWater([0, 0, 0, 0]) == 0
    assert calculateTrappedWater([3]) == 0
    assert calculateTrappedWater([1, 0, 0, 0, 0, 2]) == 4


def test_large_input():
    heights = [0] * 100000  # no peaks, should trap 0 water
    assert calculateTrappedWater(heights) == 0

    heights = [1] * 100000  # no valleys, should trap 0 water
    assert calculateTrappedWater(heights) == 0

    heights = [i % 100 for i in range(100000)]  # alternating pattern
    # can't compute exact amount but ensuring the function can handle large input
    result = calculateTrappedWater(heights)
    assert isinstance(result, int) and result >= 0


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
