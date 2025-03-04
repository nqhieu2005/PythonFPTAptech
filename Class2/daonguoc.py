def reverse_number(n):
    reversed_n = 0
    while n > 0:
        digit = n % 10
        reversed_n = reversed_n * 10 + digit
        n = n // 10
    return reversed_n


n = int(input("Nhập một số nguyên: "))
print("Số sau khi đảo ngược là:", reverse_number(n))


