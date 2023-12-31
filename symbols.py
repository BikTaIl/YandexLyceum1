string = 'qwertyuiopasdfghjklzxcvbnm!@#$%^&*-+=_1234567890'
symbols = set()
for i in string:
    symbols.add(i)
    symbols.add(i.capitalize())
print(symbols)