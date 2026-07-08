"""This script contains functions to check if a number is prime, even, and if a string is a palindrome."""

def isPrime(n):
    """Checks whether a number is prime or not."""
    if n <= 1:
        return False
    for i in range(2, n // 2):
        if n % i == 0:
            return False
    return True


def isEven(n):
    """Checks whether a number is even or not."""
    return n % 2 == 0


def isPalindrome(s):
    """Checks whether a string is a palindrome or not."""
    return s == s[::-1]


num = int(input("Enter a number: "))
text = input("Enter a string/number for palindrome check: ")

print("Prime:", isPrime(num))
print("Even:", isEven(num))
print("Palindrome:", isPalindrome(text))
