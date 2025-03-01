# Nhập vào giờ, phút, giây
gio = int(input("Nhập vào số giờ: "))
phut = int(input("Nhập vào số phút: "))
giay = int(input("Nhập vào số giây: "))

# Tính tổng số giây
tong_giay = gio * 3600 + phut * 60 + giay

# In kết quả
print("Tổng số giây tương ứng là:", tong_giay)