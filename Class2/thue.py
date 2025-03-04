def tinh_thue_thu_nhap(luong):
    if luong <= 5000000:
        thue = luong * 0.05
    elif luong <= 10000000:
        thue = 5000000 * 0.05 + (luong - 5000000) * 0.1
    elif luong <= 18000000:
        thue = 5000000 * 0.05 + 5000000 * 0.1 + (luong - 10000000) * 0.15
    else:
        thue = 5000000 * 0.05 + 5000000 * 0.1 + 8000000 * 0.15 + (luong - 18000000) * 0.2
    return thue


luong = float(input("Nhập lương: "))
thue = tinh_thue_thu_nhap(luong)
print(f"Thuế thu nhập phải đóng: {thue}")