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
