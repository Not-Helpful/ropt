import time

def ray_get(func):
    return func

# remote function
def remote_do_some_work(z):
    time.sleep(5) # Replace this with work you need to do.
    return z

def main():

    start = time.time()

    results = []
    x = 0
    y = 1

    a = remote_do_some_work(x)
    
    var1 = ray_get(a)

    b = remote_do_some_work(y) # Optimization found

    var2 = ray_get(b)

    for i in range(20):
        remoteVar = remote_do_some_work(i)
        getVar = ray_get(remoteVar)
        results.append(getVar)

    print('Total Execution Time: ', time.time() - start)

if __name__ == '__main__':
    main()
