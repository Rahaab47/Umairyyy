"""
Problem 2: Prime Number Generator
Generate all primes between 1 and user input N.
"""

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n: The number to check
        
    Returns:
        True if n is prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    
    return True

def generate_primes(n: int) -> list:
    """
    Generate all prime numbers between 1 and n (inclusive).
    
    Args:
        n: Upper limit (inclusive)
        
    Returns:
        List of prime numbers
    """
    if n < 2:
        return []
    
    primes = []
    for num in range(2, n + 1):
        if is_prime(num):
            primes.append(num)
    
    return primes

# Example usage and test cases
if __name__ == "__main__":
    print("Prime Number Generator")
    print("=" * 30)
    
    # Test with different values
    test_values = [10, 20, 30, 50]
    
    for value in test_values:
        primes = generate_primes(value)
        print(f"Primes up to {value}: {primes}")
        print(f"Count: {len(primes)}")
        print()
    
    # Interactive mode
    try:
        user_input = input("Enter a number to generate primes up to that number: ").strip()
        if user_input:
            n = int(user_input)
            primes = generate_primes(n)
            print(f"Primes up to {n}: {primes}")
            print(f"Total primes: {len(primes)}")
    except ValueError:
        print("Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\nProgram terminated.")