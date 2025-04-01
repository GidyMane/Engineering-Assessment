# fibonacci.py - Fixed Fibonacci Implementations

from functools import lru_cache

def fibonacci_recursive(n: int) -> int:
    """Efficient recursive Fibonacci using memoization."""
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    
    @lru_cache(maxsize=None)
    def fib(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    
    return fib(n)

def fibonacci_iterative(n: int) -> int:
    """Efficient iterative Fibonacci calculation."""
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    test_values = [10, 20, 30, 50]
    print("Recursive Fibonacci Results:")
    for val in test_values:
        print(f"fib({val}) = {fibonacci_recursive(val)}")
    
    print("\nIterative Fibonacci Results:")
    for val in test_values:
        print(f"fib({val}) = {fibonacci_iterative(val)}")
