from solution import longest_common_prefix

def test_longest_common_prefix_with_common_prefix():
    assert longest_common_prefix(["FLOWER", "FLOW", "FLOOR"]) == 3
    assert longest_common_prefix(["INTEREST", "INTERN", "INTERVAL"]) == 5

def test_longest_common_prefix_no_common_prefix():
    assert longest_common_prefix(["DOG", "CAT", "FISH"]) == 0

def test_longest_common_prefix_all_same():
    assert longest_common_prefix(["SAME", "SAME", "SAME"]) == 4

def test_longest_common_prefix_single_word():
    assert longest_common_prefix(["SINGLE"]) == 6

def test_longest_common_prefix_empty_list():
    assert longest_common_prefix([]) == 0

def test_longest_common_prefix_mixed_lengths():
    assert longest_common_prefix(["SHORT", "SHORTER", "SHORTEST"]) == 5   # Only matching up to "SHORT"