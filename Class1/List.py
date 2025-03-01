my_list = [1, 2, 3, 4, 5]
# print(my_list[0])
# print(my_list[-2])
# my_list.append(6)
# print(my_list)
# my_list.insert(2, 7)
# print(my_list)
# my_list.remove(7)
# print(my_list)

# for i in my_list:
#     print(i)
# # print(len(my_list))
# print(my_list.index(3))

names = ["Hiếu", "Huy", "Hà"]
names.append("Hoàng")
names.insert(1, "Hùng")
for name in names:
    print(name)

names.remove("Huy")
print(names)

name = input("Nhập tên cần tìm: ")
if name in names:
    print("Tìm thấy")
    print(names.index(name))
else:
    print("Không tìm thấy")