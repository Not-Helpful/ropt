def remote(*argv):
    pass
    
def get(*argv):
    pass

def main():

    a = 0
    b = 1
    
    remote(a)
    a = get()

    x = 10
    x = x*2

    remote(b)
    b = get()

    c = b * 5
    remote(c)
    c = get()

    data = [1, 2, 3]
    remote(data)

if __name__ == "__main__":
    main()