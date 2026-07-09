def validate_positive(func):
    def wrapper(n):
        if n < 0:
            raise ValueError("Input must be a non-negative number.")
        return func(n)
    return wrapper

@validate_positive
def square_root(n):
    return n**(1/2)

print(square_root(25))
print(square_root(0))

try:
    print(square_root(-9))
except ValueError as e:
    print(e)