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
