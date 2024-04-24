import time

def ray_get(func):
    return func

# remote function
def remote_do_some_work(x):
    time.sleep(1) # Replace this with work you need to do.
    return x


def main():

    x = 0
    y = 1

    a = remote_do_some_work(x)
    
    var1 = ray_get(a)

    b = remote_do_some_work(y) # Optimization found
    #b = remote_do_some_work(var1) # No optimization found

    var2 = ray_get(b)

    var3 = var1 + var2


if __name__ == "__main__":
    main()