def kiem_tra_chan_le(n):
    if n % 2 == 0:
        return "Chẵn"
    else:
        return "Lẻ"


n = int(input("Nhập một số nguyên: "))
print(kiem_tra_chan_le(n))