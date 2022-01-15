import time
import logging
import concurrent.futures
import threading

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="H%:%M:%S")
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class FakeDatabase:
	def __init__(self):
		self.value = 0
		self._lock = threading.Lock()

	def update(self, name):
		LOG.info("Thread %s: starting update", name)
		with self._lock:
			LOG.debug("Thread %s: get lock", name)
			local_copy = self.value
			local_copy += 1
			time.sleep(1)
			self.value = local_copy
			LOG.debug("Thread %s: release lock", name)
		LOG.info("Thread %s: finishing update", name)


if __name__ == "__main__":

		
	database = FakeDatabase()
	LOG.info("Testing update. Starting value is %d.", database.value)
	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
		for index in range(2):
			# each of the threads in the pool will call database.update(index)
			executor.submit(database.update, index)
	LOG.info("Testing update. Ending value is %d.", database.value)
