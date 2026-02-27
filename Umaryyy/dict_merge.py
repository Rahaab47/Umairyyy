"""
Problem 4: Dictionary Merge
Merge two dictionaries; if keys overlap, sum their values.
"""

def merge_dictionaries(dict1: dict, dict2: dict) -> dict:
    """
    Merge two dictionaries. If keys overlap, sum their values.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary with summed values for overlapping keys
    """
    # Create a copy of the first dictionary to avoid modifying the original
    merged = dict1.copy()
    
    # Iterate through the second dictionary
    for key, value in dict2.items():
        if key in merged:
            # If key exists in both, sum the values
            merged[key] += value
        else:
            # If key only exists in dict2, add it
            merged[key] = value
    
    return merged

# Alternative implementation using dictionary comprehension and collections.Counter
def merge_dictionaries_v2(dict1: dict, dict2: dict) -> dict:
    """
    Merge two dictionaries using Counter for cleaner code.
    """
    from collections import Counter
    return dict(Counter(dict1) + Counter(dict2))

# Example usage and test cases
if __name__ == "__main__":
    print("Dictionary Merge")
    print("=" * 30)
    
    # Test cases
    test_cases = [
        ({'a': 1, 'b': 2}, {'b': 3, 'c': 4}),
        ({'x': 5, 'y': 10}, {'y': -3, 'z': 7}),
        ({}, {'a': 1, 'b': 2}),
        ({'key': 100}, {'key': 200}),
        ({'a': 1.5, 'b': 2.5}, {'b': 3.5, 'c': 4.5})
    ]
    
    for i, (d1, d2) in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"  Dict1: {d1}")
        print(f"  Dict2: {d2}")
        
        result1 = merge_dictionaries(d1, d2)
        result2 = merge_dictionaries_v2(d1, d2)
        
        print(f"  Result (Method 1): {result1}")
        print(f"  Result (Method 2): {result2}")
        print(f"  Match: {result1 == result2}")
        print()
    
    # Interactive mode
    try:
        print("Interactive Dictionary Merge:")
        print("Enter first dictionary (key:value pairs separated by spaces, e.g., 'a:1 b:2'):")
        input1 = input().strip()
        dict1 = {}
        if input1:
            pairs = input1.split()
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    dict1[key] = float(value) if '.' in value else int(value)
        
        print("Enter second dictionary (same format):")
        input2 = input().strip()
        dict2 = {}
        if input2:
            pairs = input2.split()
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    dict2[key] = float(value) if '.' in value else int(value)
        
        result = merge_dictionaries(dict1, dict2)
        print(f"Merged dictionary: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram terminated.")