"""This script contains functions to check if a number is 
prime, even, and if a string is a palindrome."""

def is_prime(n):
    """Checks whether a number is prime or not."""
    if n <= 1:
        return False
    for i in range(2, n // 2):
        if n % i == 0:
            return False
    return True


def is_even(n):
    """Checks whether a number is even or not."""
    return n % 2 == 0


def is_palindrome(s):
    """Checks whether a string is a palindrome or not."""
    return s == s[::-1]


num = int(input("Enter a number: "))
text = input("Enter a string/number for palindrome check: ")

print("Prime:", is_prime(num))
print("Even:", is_even(num))
print("Palindrome:", is_palindrome(text))
