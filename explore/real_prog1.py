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

    a = do_some_work.remote(x)
    b = do_some_work.remote(y)

    r1_results = ray.get(a)
    r2_results = ray.get(b)

    print("Total Execution Time: ", time.time() - start)

if __name__ == "__main__":
    main()