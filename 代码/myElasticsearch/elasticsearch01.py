#!/usr/bin/env/python
# coding=UTF-8
'''
python连接es
'''
row = ["I", "love", "python"]
print(*row)
print(*row, sep=" ")
# method-2
print(' '.join(row))

print(['L', 'G', 'PK'][::-1])


def check_up(x):
    if x.isalpha():
        return x.lower()
    else:
        return ' '


x = list(map(check_up,"382HcskK"))
print(x)
