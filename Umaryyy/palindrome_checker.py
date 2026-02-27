"""
Problem 1: Palindrome Checker
Function to detect palindromes (ignore spaces, punctuation, case).
"""

import re

def is_palindrome(text: str) -> bool:
    """
    Check if a string is a palindrome, ignoring spaces, punctuation, and case.
    
    Args:
        text: The string to check
        
    Returns:
        True if the string is a palindrome, False otherwise
        
    Examples:
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("race a car")
        False
        >>> is_palindrome("Madam")
        True
    """
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    
    # Check if the cleaned text is equal to its reverse
    return cleaned_text == cleaned_text[::-1]

# Example usage and test cases
if __name__ == "__main__":
    test_cases = [
        "A man a plan a canal Panama",
        "race a car",
        "Madam",
        "No 'x' in Nixon",
        "Mr. Owl ate my metal worm",
        "12321",
        "hello world",
        ""
    ]
    
    print("Palindrome Checker Test Results:")
    print("-" * 40)
    for test in test_cases:
        result = is_palindrome(test)
        print(f"'{test}' -> {result}")