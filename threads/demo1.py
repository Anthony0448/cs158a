import threading
import time


def sayhello(id, sleep):
    print(f"Hello from Thread {id}")

    time.sleep(sleep)


# TODO: you should have 10 threads
num_threads = 10
threads = []

for id in range(num_threads):
    t = threading.Thread(target=sayhello, args=(id,),
                         # Pass arguments to function
                         kwargs={"sleep": 10})

    threads.append(t)

stime = time.time()

# TODO: start all 10 threads
for t in threads:
    t.start()

# TODO: Wait for all threads to finish
for t in threads:
    t.join()

etime = time.time()

print("Time taken: ", etime - stime)
