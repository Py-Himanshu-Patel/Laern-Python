# Multi Threading

### Threading - without daemon

```python
import logging
import threading
import time

def thread_function(name):
	logging.info("Thread %s	:	starting", name)
	time.sleep(2)
	logging.info("Thread %s	:	finishing", name)

if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
	logging.info("Main		:	Before creating thread")
	x = threading.Thread(target=thread_function, args=(1,))
	logging.info("Main		:	Before running thread")
	x.start()
	logging.info("Main		:	wait for the thread to finish")
	# x.join()
	logging.info("Main		:	all done")
```

```bash
14:15:36: Main          :       Before creating thread
14:15:36: Main          :       Before running thread
14:15:36: Thread 1      :       starting
14:15:36: Main          :       wait for the thread to finish
14:15:36: Main          :       all done
14:15:38: Thread 1      :       finishing
```

- Here we have two thread one is `main` thread and another we started with `threading.Thread`.
- A **daemon** is a process that runs in the background.
- If a program is running **Threads** that are not **daemons**, then the program will wait for those threads to complete before it terminates. **Threads** that are **daemons**, however, are just killed wherever they are when the program is exiting.
- The pause when before the last line get printed is actually Python waiting for the **non-daemonic** thread to complete. When your Python program ends, part of the shutdown process is to clean up the threading routine.
- `threading._shutdown()` walks through all of the running threads and calls `.join()` on every one that does not have the daemon flag set. So your program waits to exit because the thread itself is waiting in a sleep.

### Threading - with daemon

```python
x = threading.Thread(target=thread_function, args=(1,), daemon=True)
```

Again running the programm gives the output

```bash
14:33:41: Main          :       Before creating thread
14:33:41: Main          :       Before running thread
14:33:41: Thread 1      :       starting
14:33:41: Main          :       wait for the thread to finish
14:33:41: Main          :       all done
```

The difference here is that the final line of the output is missing. `thread_function()` did not get a chance to complete. It was a daemon thread, so when `__main__` reached the end of its code and the program wanted to finish, the daemon was killed.

To tell one thread to wait for another thread to finish, you call `.join()`. If you uncomment that line `x.join()`, the main thread will pause and wait for the thread x to complete running.

### Multiple Threads - Manual Handeling

```python
import logging
import threading
import time


def thread_function(name):
	logging.info("Thread %s: starting", name)
	time.sleep(4)
	logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
	
	threads = list()
	for index in range(3):
		logging.info("Main	:	create and start thread %d.", index)
		x = threading.Thread(target=thread_function, args=(index,))
		threads.append(x)
		x.start()

	for index, thread in enumerate(threads):
		logging.info("Main	:	before joining thread %d", index)
		thread.join()
		logging.info("Main	:	thread %d done", index)
```

```bash
16:17:04: Main  :       create and start thread 0.
16:17:04: Thread 0: starting
16:17:04: Main  :       create and start thread 1.
16:17:04: Thread 1: starting
16:17:04: Main  :       create and start thread 2.
16:17:04: Thread 2: starting
16:17:04: Main  :       before joining thread 0
16:17:08: Thread 0: finishing
16:17:08: Main  :       thread 0 done
16:17:08: Thread 2: finishing
16:17:08: Thread 1: finishing
16:17:08: Main  :       before joining thread 1
16:17:08: Main  :       thread 1 done
16:17:08: Main  :       before joining thread 2
16:17:08: Main  :       thread 2 done
```

The order in which threads are run is determined by the operating system and can be quite hard to predict. 

### Multiple Threads - ThreadPoolExecutor

The easiest way to create it is as a **context manager**, using the `with` statement to manage the creation and destruction of the pool.

```python
import logging
import time
import concurrent.futures


def thread_function(name):
	logging.info("Thread %s: starting", name)
	time.sleep(4)
	logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

	logging.info("Before Thread pool")
	with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		executor.map(thread_function, range(3))
	logging.info("After Thread pool")
```

```bash
19:39:32: Before Thread pool
19:39:32: Thread 0: starting
19:39:32: Thread 1: starting
19:39:32: Thread 2: starting
19:39:36: Thread 1: finishing
19:39:36: Thread 0: finishing
19:39:36: Thread 2: finishing
19:39:36: After Thread pool
```

Again, notice how Thread 1 finished before Thread 0. The scheduling of threads is done by the operating system and does not follow a plan that’s easy to figure out.

### Race Conditions 

Race conditions can occur when two or more threads access a shared piece of data or resource. In this example, you’re going to create a large race condition that happens every time, but be aware that most race conditions are not this obvious. Frequently, they only occur rarely, and they can produce confusing results. As you can imagine, this makes them quite difficult to debug.

```python
import time
import logging
import concurrent.futures


class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("Thread %s: finishing update", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
        
    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            # each of the threads in the pool will call database.update(index)
            executor.submit(database.update, index)
    logging.info("Testing update. Ending value is %d.", database.value)
```

```bash
20:30:25: Testing update. Starting value is 0.
20:30:25: Thread 0: starting update
20:30:25: Thread 1: starting update
20:30:25: Thread 0: finishing update
20:30:25: Thread 1: finishing update
20:30:25: Testing update. Ending value is 1.
```

The program creates a `ThreadPoolExecutor` with two threads and then calls `.submit()` on each of them, telling them to run `database.update()`. `.submit()` has a signature that allows both positional and named arguments to be passed to the function running in the thread:

```python
.submit(function, *args, **kwargs)
```

When the thread starts running `.update()`, it has its own version of all of the data local to the function. In the case of `.update()`, this is `local_copy`. This is definitely a good thing. Otherwise, two threads running the same function would always confuse each other. It means that all variables that are scoped (or local) to a function are **thread-safe**.

In case of two thread they will each have their own version of `local_copy` and will each point to the same database. It is this shared database object that is going to cause the problems. When Thread 1 calls `time.sleep()`, it allows the other thread to start running. The two threads have interleaving access to a single shared object, overwriting each other’s results. Similar race conditions can arise when one thread frees memory or closes a file handle before the other thread is finished accessing it.

### Basic Synchronization Using Lock

