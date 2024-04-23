def remote(*argv):
    pass
    
def get(*argv):
    return 2

def func():
    return 1

def func2(arg):
    return arg + 1

def doThings(a, b):
    return (a + b)

# def func3(arg, listA):
#     listA.append(arg)

class classA():

    def __init__(self):
        self.z = 7


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

    newClass = classA()

    x = newClass.z

    for i in range(6):
        var = var + 1

    listB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    listC = []

    for i in range(10):
        listC.append(doThings(listB[i], var))
        
    print(listC)

    # func3(x, data)

if __name__ == "__main__":
    main()