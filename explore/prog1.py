import time

def ray_get(func):
    return func

# remote function
def remote_do_some_work(x):
    time.sleep(5) # Replace this with work you need to do.
    return x


def main():

    x = 0
    y = 1

    a = remote_do_some_work(x)
    
    var1 = ray_get(a)

    b = remote_do_some_work(y) # Optimization found

    var2 = ray_get(b)

    var3 = var1 + var2


if __name__ == "__main__":
    main()