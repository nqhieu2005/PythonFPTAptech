def print_triangle(h):
    for i in range(1, h + 1):
        print('*' * i)

if __name__ == "__main__":
    h = int(input("Nhập số nguyên h: "))
    print_triangle(h)