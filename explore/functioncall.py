#!/usr/bin/env python3

import dis

a = 5

def funccall():
    a = 3
    b = 2
    callme(a, b)

def callme(a):
    print(a)



print(dis.dis(funccall))

for ins in dis.Bytecode(funccall):
    print(ins)
