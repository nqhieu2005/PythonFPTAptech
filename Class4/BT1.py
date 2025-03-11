class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print("Name:", self.name)
        print("Age:", self.age)

    def __str__(self):
        return "Name: " + self.name + ", Age: " + str(self.age)

s = Student("John", 21)
s.display()
print(s)