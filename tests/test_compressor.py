import pytest
from minicahe.compressor import compress_text

def test_acronymizer_collision():
    # Setup a scenario where two different N-grams share the same initials
    text = "The natural language processing system handles national library policy very well. Both natural language processing and national library policy are important."
    
    # In the old code, both would become "NLP", leading to collision.
    # In the new code, the first one gets "NLP", the second one is ignored because "NLP" is already in used_acronyms.
    
    compressed = compress_text(text, aggressive=True)
    
    # Check that "NLP" appears
    assert "NLP" in compressed
    
    # Check that the second phrase is still preserved somewhat (since it couldn't be acronymized to NLP)
    # The actual compression might drop some words, but it shouldn't be "NLP" twice.
    # If the first was acronymized, "NLP" replaces "natural language processing".
    # The second "national library policy" will remain words. 
    # Let's count "NLP". Since "natural language processing" appeared twice, "NLP" should appear twice.
    # If there was a collision, "NLP" would appear 4 times (replacing all 4).
    
    nlp_count = compressed.count("NLP")
    assert nlp_count == 2
    
def test_preserve_words_flag():
    text = "This api and url are crucial for the sql query."
    compressed = compress_text(text, aggressive=True, preserve_words=['api', 'url', 'sql'])
    assert 'api' in compressed
    assert 'url' in compressed
    assert 'sql' in compressed

def test_no_acronym_flag():
    text = "The central processing unit is very fast. The central processing unit is expensive."
    compressed_with = compress_text(text, aggressive=True)
    compressed_without = compress_text(text, aggressive=True, no_acronym=True)
    
    assert "CPU" in compressed_with
    assert "CPU" not in compressed_without

def test_sentence_dedup():
    text = "Hello world. Hello universe! Hello galaxy?"
    compressed = compress_text(text, aggressive=True)
    # Because 'hello' is followed by punctuation in earlier processing, or punctuation clears the set,
    # it should appear multiple times.
    # Wait, 'hello' appears at the start, then 'world.', which ends with '.'. So after 'world.', the set is cleared.
    # This means 'hello' will be preserved in the next sentence.
    assert compressed.lower().count("hello") == 3

def test_logical_blacklist():
    text = "The vendor shall not be liable for the damages. No exceptions will be made. I will never agree."
    compressed = compress_text(text, aggressive=True)
    # Even in aggressive mode, 'not', 'no', 'never' should survive.
    assert "not" in compressed.lower()
    assert "no" in compressed.lower()
    assert "never" in compressed.lower()

def test_conservative_mode():
    text = "The quick brown fox jumps over the lazy dog. The quick brown fox is very fast."
    compressed_agg = compress_text(text, mode="aggressive")
    compressed_con = compress_text(text, mode="conservative")
    
    # Aggressive drops "the", "is", "very"
    assert "very" not in compressed_agg.lower()
    
    # Conservative drops duplicate "quick", "brown", "fox" but keeps "the", "is", "very"
    assert "very" in compressed_con.lower()
    assert "the" in compressed_con.lower()
    
    # The second "quick brown fox" (and the first) will actually be replaced by QBF!
    # Because auto-acronymizer is active in both modes.
    assert "qbf" in compressed_con.lower()
    assert "quick" not in compressed_con.lower()

def test_pii_masking():
    text = "Contact me at john.doe@example.com or call 123-456-7890."
    compressed = compress_text(text, aggressive=True, mask_pii=True)
    assert "john.doe@example.com" not in compressed
    assert "[EMAIL]" in compressed
    assert "[REDACTED]" in compressed

def test_bug_1_and_3_fixes():
    # Bug 1: key, use, was should not be stripped even though length is 3
    text1 = "The key feature is that we use this API. Error was caused by null pointer."
    compressed1 = compress_text(text1, aggressive=True)
    assert "key" in compressed1.lower()
    assert "use" in compressed1.lower()
    assert "was" in compressed1.lower()

    # Bug 3: alphanumeric whitelist like v2, v3 shouldn't be broken by stripping numbers
    text2 = "Use API v2 to call GET /id and POST /add"
    compressed2 = compress_text(text2, aggressive=True)
    assert "v2" in compressed2.lower()
    # "add" will be dropped because it's < 4 chars and not in whitelist.

if __name__ == "__main__":
    pytest.main([__file__])

