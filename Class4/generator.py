def event_numbers(n):
    for i in range(0, n, 2):
            yield i
gen =  event_numbers(10)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen)) 
print(next(gen))
