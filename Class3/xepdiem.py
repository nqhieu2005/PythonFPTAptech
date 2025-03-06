


def nhap_danh_sach():
    danh_sach = []
    so_luong_hoc_sinh = int(input("Nhập số lượng học sinh: "))
    for i in range(so_luong_hoc_sinh):
        ten = input(f"Nhập tên học sinh thứ {i + 1}: ")
        diem = float(input(f"Nhập điểm của học sinh {ten}: "))
        danh_sach.append((ten, diem))
    return danh_sach


def sap_xep_danh_sach(danh_sach):
    return sorted(danh_sach, key=lambda x: x[1], reverse=True)


def hien_thi_danh_sach(danh_sach):
    for ten, diem in danh_sach:
        print(f"Học sinh: {ten}, Điểm: {diem}")


if __name__ == "__main__":
    danh_sach_hoc_sinh = nhap_danh_sach()
    danh_sach_sap_xep = sap_xep_danh_sach(danh_sach_hoc_sinh)
    print("\nDanh sách học sinh sau khi sắp xếp theo điểm từ cao xuống thấp:")
    hien_thi_danh_sach(danh_sach_sap_xep)