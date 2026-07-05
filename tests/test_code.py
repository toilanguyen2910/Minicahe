import pytest
from minicahe.compressor import compress_text

def test_code_compressor():
    text = """def process_data(data: list) -> dict:
    \"\"\"
    Process the input data list and return a dictionary of results.
    This function filters out None values and calculates the sum.
    \"\"\"
    # Initialize the result dictionary
    result = {'valid_items': 0, 'total_sum': 0}
    
    for item in data:
        # Check if the item is valid
        if item is not None:
            result['valid_items'] += 1
            result['total_sum'] += item
            
    return result
"""
    compressed = compress_text(text, aggressive=True, code=True)
    
    # Assert that docstring is removed
    assert "Process the input data list" not in compressed
    
    # Assert that comments are removed
    assert "Initialize the result dictionary" not in compressed
    
    # Assert that actual code logic is preserved
    assert "def process_data(data: list) -> dict:" in compressed
    assert "result = {'valid_items': 0, 'total_sum': 0}" in compressed
    assert "return result" in compressed

def test_standalone_string_is_stripped():
    text = """def foo():
    \"\"\"This is a docstring\"\"\"
    a = "This is a normal string"
    \"\"\"This is another standalone string\"\"\"
    return a
"""
    compressed = compress_text(text, aggressive=True, code=True)
    assert "This is a docstring" not in compressed
    assert "This is another standalone string" not in compressed
    assert "This is a normal string" in compressed  # Should NOT be stripped because it's assigned to a variable

def test_universal_code_stripper_fallback():
    # A snippet of JS code that breaks python parser
    text = """function calculate(a, b) {
    /*
     * This is a block comment
     */
    // This is a line comment
    let sum = a + b;
    return sum;
}
"""
    # This will fail ast/tokenize and fallback to _regex_compress
    compressed = compress_text(text, aggressive=True, code=True)
    assert "This is a block comment" not in compressed
    assert "This is a line comment" not in compressed
    assert "function calculate" in compressed
    assert "let sum" in compressed

def test_universal_code_stripper_edge_cases():
    text = """function test() {
    let url = "https://example.com";
    let block = "/* not a comment */";
    // actual comment
    return url;
}
"""
    compressed = compress_text(text, aggressive=True, code=True)
    assert "https://example.com" in compressed
    assert "/* not a comment */" in compressed
    assert "actual comment" not in compressed

if __name__ == "__main__":
    pytest.main([__file__])
