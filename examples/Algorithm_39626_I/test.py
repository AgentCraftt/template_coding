from solution import can_form_word

def test_can_form_word_true():
    assert can_form_word("aabbcc", "abc") == True
    assert can_form_word("aabbcc", "abccba") == True
    assert can_form_word("aabbcc", "aabbcc") == True

def test_can_form_word_false():
    assert can_form_word("aabbcc", "abcd") == False
    assert can_form_word("aabbcc", "aabbccc") == False
    assert can_form_word("aabbcc", "bbaaadd") == False

def test_can_form_word_with_extra_tiles():
    assert can_form_word("aabbccddeeff", "abc") == True
    assert can_form_word("aabbccddeeff", "abcd") == True
    assert can_form_word("aabbccddeeff", "ddeeff") == True

def test_can_form_word_empty_cases():
    assert can_form_word("", "") == True
    assert can_form_word("abc", "") == True
    assert can_form_word("", "abc") == False