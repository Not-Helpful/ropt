import time

def ray_get(func):
    return func

# remote function
def remote_do_some_work(x):
    time.sleep(1) # Replace this with work you need to do.
    return x

def main():
    start = time.time()

    results = []

    for x in range(4):
        results.append(ray_get(remote_do_some_work(x)))
    
    print("duration =", time.time() - start)
    print("results =", results)

if __name__ == '__main__':
    main()