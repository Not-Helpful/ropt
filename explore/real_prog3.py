import time
import ray


@ray.remote
def do_some_work(x):
    time.sleep(5) # Replace this with work you need to do.
    return x

def main():

    start = time.time()

    x = 0
    y = 1
    results = []
    c = []

    a = do_some_work.remote(x)

    b = do_some_work.remote(y)

    for x in range(20):
        c = do_some_work.remote(x)
        # results.append(ray.get(c))

    r1_results = ray.get(a)
    r2_results = ray.get(b)
    results = ray.get(c)

    print("Total Execution Time: ", time.time() - start)

if __name__ == "__main__":
    main()