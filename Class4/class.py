class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

car1 = Car('Toyota', 'Corolla')
print(car1.brand)

class Account:
    def __init__(self, balance):
        self.__balance = balance # private attribute

class Person:
    def __init__(self, name):
        self.name = name