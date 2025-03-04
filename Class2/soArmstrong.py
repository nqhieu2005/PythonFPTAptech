def is_armstrong_number(n):
    num_str = str(n)
    num_len = len(num_str)
    sum_of_powers = sum(int(digit) ** num_len for digit in num_str)
    return sum_of_powers == n

# Input: Một số nguyên n
n = int(input("Nhập một số nguyên: "))

# Output: "Là số Armstrong" hoặc "Không phải số Armstrong"
if is_armstrong_number(n):
    print("Là số Armstrong")
else:
    print("Không phải số Armstrong")