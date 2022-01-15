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
