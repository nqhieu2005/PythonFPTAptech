def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def primes_less_than_n(N):
    primes = []
    for num in range(2, N):
        if is_prime(num):
            primes.append(num)
    return primes

# Input
N = int(input("Nhập số nguyên N: "))

# Output
print("Các số nguyên tố nhỏ hơn", N, "là:", primes_less_than_n(N))