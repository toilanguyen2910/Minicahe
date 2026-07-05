from minicahe.compressor import compress_text
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
print("--- OUTPUT ---")
print(compress_text(text, aggressive=True, code=True))
