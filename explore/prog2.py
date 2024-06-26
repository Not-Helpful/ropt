import time

def ray_get(func):
    return func

# remote function
def remote_do_some_work(x):
    time.sleep(5) # Replace this with work you need to do.
    return x

def main():

    start = time.time()

    results = []
    
    for x in range(10):
        remoteVar = remote_do_some_work(x)
        getVar = ray_get(remoteVar)
        results.append(getVar)


    print('Total Execution Time: ', time.time() - start)

if __name__ == '__main__':
    main()
