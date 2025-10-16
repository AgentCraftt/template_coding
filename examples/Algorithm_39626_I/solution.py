from collections import Counter

def can_form_word(tiles: str, word: str) -> bool:
    """
    Check if a given word can be formed using the given tiles.
    """
    tile_count = Counter(tiles)
    word_count = Counter(word)
    
    for char, count in word_count.items():
        if tile_count[char] < count:
            return False
    
    return True