"""
Problem 3: List Analysis
Return:
- Maximum
- Minimum
- Average
- Numbers above average
"""

def analyze_list(numbers: list) -> dict:
    """
    Analyze a list of numbers and return statistics.
    
    Args:
        numbers: List of numbers (int or float)
        
    Returns:
        Dictionary with keys: 'max', 'min', 'average', 'above_average'
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("List cannot be empty")
    
    # Calculate maximum and minimum
    max_val = max(numbers)
    min_val = min(numbers)
    
    # Calculate average
    average = sum(numbers) / len(numbers)
    
    # Find numbers above average
    above_average = [num for num in numbers if num > average]
    
    return {
        'max': max_val,
        'min': min_val,
        'average': average,
        'above_average': above_average
    }

# Example usage and test cases
if __name__ == "__main__":
    print("List Analysis")
    print("=" * 30)
    
    # Test cases
    test_cases = [
        [1, 2, 3, 4, 5],
        [10, 20, 30, 40, 50],
        [-5, -2, 0, 3, 7],
        [42],
        [1.5, 2.5, 3.5, 4.5]
    ]
    
    for i, numbers in enumerate(test_cases, 1):
        print(f"Test Case {i}: {numbers}")
        try:
            result = analyze_list(numbers)
            print(f"  Maximum: {result['max']}")
            print(f"  Minimum: {result['min']}")
            print(f"  Average: {result['average']:.2f}")
            print(f"  Above Average: {result['above_average']}")
        except ValueError as e:
            print(f"  Error: {e}")
        print()
    
    # Interactive mode
    try:
        user_input = input("Enter numbers separated by spaces: ").strip()
        if user_input:
            numbers = [float(x) for x in user_input.split()]
            result = analyze_list(numbers)
            print(f"\nAnalysis Results:")
            print(f"Maximum: {result['max']}")
            print(f"Minimum: {result['min']}")
            print(f"Average: {result['average']:.2f}")
            print(f"Numbers above average: {result['above_average']}")
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram terminated.")