def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, n //2):
        if n % i == 0:
            return False
    return True

def isEven(n):
    return n % 2 == 0

def isPalindrome(s):
    return s == s[::-1]

num = int(input("Enter a number: "))
text = input("Enter a string/number for palindrome check: ")

print("Prime:", isPrime(num))
print("Even:", isEven(num))
print("Palindrome:", isPalindrome(text))