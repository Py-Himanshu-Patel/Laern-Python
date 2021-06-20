import asyncio
import time

async def coroutine(lst):
	''' IO wait time is proportional to max element in list '''
	await asyncio.sleep(max(lst))
	return list(reversed(lst))


async def main():
	lst = [-3, -1, 1]
	task1 = asyncio.create_task(coroutine(lst))
	lst = [-1, 0, 1]
	task2 = asyncio.create_task(coroutine(lst))

	start = time.perf_counter()
	result = await asyncio.gather(task1, task2)
	end = time.perf_counter()
	print(f"Both tasks done: {all([task1.done(), task2.done()])}")
	print(f"Time taken: {(end - start):0.5f} seconds")
	return result

res = asyncio.run(main())
print(res)
