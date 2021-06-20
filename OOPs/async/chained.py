import asyncio
import random
import time


async def first(n: int) -> str:
    ''' first coroutine '''

    i = random.randint(0, 10)
    print(f"first({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    print()
    print(f"Returning first({n})")
    return f"first-{n}"

async def second(n: int, arg: str) -> str:
    ''' second coroutine '''

    i = random.randint(0, 10)
    print(f"second({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    print(f"Returning second({n})")
    return f"second-{arg}"

async def chain(n: int) -> None:
    ''' chaining both coroutine '''

    start = time.perf_counter()
    p1 = await first(n)
    p2 = await second(n, p1)
    end = time.perf_counter() - start
    print()
    print(f"-->Chained: {n} => {p1} => {p2} (took {end:0.2f} seconds).")
    print()

async def main(*args):
    await asyncio.gather(*(chain(n) for n in args))


if __name__ == "__main__":
    import sys
    random.seed(100)
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    start = time.perf_counter()
    asyncio.run(main(*args))
    end = time.perf_counter() - start
    print(f"Program finished in {end:0.2f} seconds.")
