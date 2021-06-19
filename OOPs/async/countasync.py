import asyncio

async def count():
	print("One")
	await asyncio.sleep(1)
	print("Two")

async def main():
	await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
	import time
	from pathlib import Path
	file_name = Path(__file__).name
	start = time.perf_counter()
	asyncio.run(main())
	elapsed = time.perf_counter() - start

	print(f"{file_name} executed in {elapsed:0.2f} seconds.")

