from solution import can_form_anagram


def test_basic_anagrams():
    assert can_form_anagram("aabb", "bbaa", 0) == True
    assert can_form_anagram("cat", "tac", 0) == True
    assert can_form_anagram("listen", "silent", 0) == True


def test_character_removal_cases():
    assert can_form_anagram("aabb", "bbbaaa", 2) == True
    assert can_form_anagram("abc", "abcd", 1) == True
    assert can_form_anagram("aabb", "aaaabbbb", 4) == True


def test_false_cases():
    assert can_form_anagram("aabb", "bbaa", 1) == False
    assert can_form_anagram("abc", "abcde", 1) == False
    assert can_form_anagram("abc", "def", 1) == False


def test_edge_cases():
    assert can_form_anagram("", "", 0) == True
    assert can_form_anagram("a", "a", 0) == True
    assert can_form_anagram("a", "b", 1) == False
