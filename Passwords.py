from sys import stdin

passwords_list = []
for i in stdin:
    password = i.strip()
    passwords_list.append(password.lower())
passwords_list.remove(passwords_list[-1])
while '' in passwords_list:
    passwords_list.remove('')
print(passwords_list)