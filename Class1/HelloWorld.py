print("Hello, my name is Hieu")
print(98.6)
x = int(98.6)
print(x)
# age = 20
# if age < 18:
#     print("Bạn chưa đủ 18 tuổi")
# elif age == 18:
#     print("Chúc mừng bạn đã đủ 18 tuổi")
# else:
#     print("Bạn đã trưởng thành") 
# n = 10

# for i in range(1, n, 2 ):
#     print(i)

# while n > 0:
#     print(n)
#     n -= 1

# def greet(name = "World"):  
#     return "Hello " + name

# print(greet())  

# print(greet("Hiếu"))

# name = input("Nhập tên của bạn: ")
# print(greet(name))

# hrs = input("Enter Hours:")
# salary = input("Enter your salary:")
# Tong = float(hrs) * float(salary)
# print("Pay:", Tong)

# def is_palindrome(number):
    
#     str_number = str(number)
    
#     return str_number == str_number[::-1]


# number = int(input("Enter a number: "))
# if is_palindrome(number):
#     print(f"{number} is a palindrome.")
# else:
#     print(f"{number} is not a palindrome.")

def number_to_words(number):
    num_to_word = {
        '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
        '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
    }
    
    return ' '.join(num_to_word[digit] for digit in str(number))

number = int(input("Enter a number: "))
print(number_to_words(number))

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

