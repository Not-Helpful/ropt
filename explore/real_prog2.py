import time
import ray

@ray.remote
def do_some_work(x):
    time.sleep(5) # Replace this with work you need to do.
    return x

def main():

    start = time.time()

    results = []
    a = []

    for x in range(10):
        a = do_some_work.remote(x)
        # results.append(ray.get(a))

    results = ray.get(a)

    print("Total Execution Time: ", time.time() - start)

if __name__ == "__main__":
    main()