def kiem_tra_nam_nhuan(y):
    if (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0):
        return "Năm nhuận"
    else:
        return "Không phải năm nhuận"


nam = int(input("Nhập năm cần kiểm tra: "))
print(kiem_tra_nam_nhuan(nam))