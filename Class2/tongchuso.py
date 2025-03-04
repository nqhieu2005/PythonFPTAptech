n = input("Nhập một số: ")
n = int(n)

sum_of_digits = sum(int(digit) for digit in str(n))
print("Tổng các chữ số của số vừa nhập là:", sum_of_digits)