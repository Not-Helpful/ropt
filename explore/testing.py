def remote(*argv):
    pass
    
def get(*argv):
    pass

def func():
    return 1

def func2(arg):
    return arg + 1

def main():

    a = 0
    b = 1
    c = a + b
    d = c * 2
    e = func() + c
    f = func2(d) + b
    g = e + f

    remote(a)
    a = get()

    x = 10
    x = x*2

    remote(b)
    b = get()

    c = b * 5
    remote(c)
    c = get()

    data = [c, e, g]
    remote(data)

    var = b

    data.append(a)

    if(a > f):
        print('impossible')
    elif(f > a):
        print('possible')
    else:
        print('impossible, again')

if __name__ == "__main__":
    main()