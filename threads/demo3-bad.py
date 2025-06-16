import threading
import time

# Global variable
counter = 0

def increment():
    global counter
    
    for _ in range(1000):
        temp = counter

        time.sleep(0.0001)

        counter = temp + 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()

t1.join()
t2.join()

print("Counter value: ", counter)