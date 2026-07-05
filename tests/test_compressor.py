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

if __name__ == "__main__":
    pytest.main([__file__])
