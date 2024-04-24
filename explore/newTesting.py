import time

def ray_get(func):
    return func

# remote function
def remote_do_some_work(x):
    time.sleep(1) # Replace this with work you need to do.
    return x

def main():

    results = []

    for x in range(4):
        remoteVar = remote_do_some_work(x)
        getVar = ray_get(remoteVar)
        results.append(getVar)

if __name__ == '__main__':
    main()




    


    