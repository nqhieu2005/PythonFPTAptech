try:
    
    result = 10 / 0
except ZeroDivisionError:
    
    print("Error: Division by zero is not allowed.")
else:
    
    print("The result is:", result)
finally:
   
    print("Execution completed.")