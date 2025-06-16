import threading
import time


class Greeter(threading.Thread):
    # Is this lowkey just a constructor.....
    def __init__(self, id, sleep):
        threading.Thread.__init__(self)
        self.id = id
        self.sleep = sleep

    def run(self):
        print(f"Hello from Thread {self.id}!")
        time.sleep(self.sleep)


threads = []
num_threads = 10

for id in range(num_threads):
    # Instantiate and pass arguments
    t = Greeter(id, 5)

    threads.append(t)

stime = time.time()
for t in threads:
    t.start()

for t in threads:
    t.join()

etime = time.time()
print("Time taken: ", etime - stime)
