# Asynchronous IO

## Concurrency

If there are two tasks T1 and T2 and executing both of them on single core. For sometime T1 execute and for some time T2 execute this make user feel both the functionality are accessible and application appears to be interactive. This is usefull when we want to make application responsive and not to complete all the task quickly utilizing all the cores of processor. Usefull when complete completion of both thread is not usefull but simultaneous exeution is usefull.

Concurrency is achieved through the interleaving operation of processes on the central processing unit(CPU) or in other words by the context switching.

## Multiprocessing / Parallelism

If there are two task T1 and T2 then exexuting both of them on different core C1 and C2 parallely is Parallelism. This is usefull then we want to complete said task fast completely. Usefull when complete execution of both task is usefull while simultaneous execution or completion of one before other is not usefull.

It is achieved by through multiple central processing units(CPUs) and cannot be achieved via single CPU.

## Threading

Threading is a concurrent execution model whereby multiple threads take turns executing tasks. One process can contain multiple threads. Threading is better for IO-bound tasks.

### Note 2

- **Concurrency** does not imply **Parallelism**.
- `Concurrency` encompasses both `Multiprocessing` (ideal for CPU-bound tasks) and `Threading` (suited for IO-bound tasks).

## Asynchronous

- `async/await`: two new Python keywords that are used to define **coroutines**.
- `asyncio`: the Python package that provides a foundation and API for running and managing **coroutines**.
- `async IO` is not threading, nor is it multiprocessing. It is not built on top of either of these.
- `async IO` is a single-threaded, single-process design: it uses cooperative multitasking. It has been said in other words that async IO gives a feeling of concurrency despite using a single thread in a single process. Coroutines (a central feature of async IO) can be scheduled concurrently, but they are not inherently concurrent.

Asynchronous routines are able to “pause” while waiting on their ultimate result and let other routines run in the meantime.

## Coroutine

A coroutine is a specialized version of a Python generator function. A coroutine is a function that can suspend its execution before reaching return, and it can indirectly pass control to another coroutine for some time.

## asyncio Package

```python
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
```

```bash
One
One
One
Two
Two
Two
countasync.py executed in 1.17 seconds.
```

When each task reaches `await asyncio.sleep(1)`, the function yells up to the event loop and gives control back to it, saying, “I’m going to be sleeping for 1 second. Go ahead and let something else meaningful be done in the meantime.”

`time.sleep()` can represent any time-consuming blocking function call, while `asyncio.sleep()` is used to stand in for a non-blocking call (but one that also takes some time to complete).

### The Rules of Async IO

- The syntax `async def` introduces either a **native coroutine** or an **asynchronous generator**. The expressions `async with` and `async for` are also valid.

- The keyword `await` passes function control back to the event loop. (It suspends the execution of the surrounding coroutine.) If Python encounters an `await f()` expression in the scope of `g()`, this is how `await` tells the event loop, “Suspend execution of `g()` until whatever I’m waiting on—the result of `f()`—is returned. In the meantime, go let something else run.”

```python
async def g():
    # Pause here and come back to g() when f() is ready
    r = await f()
    return r
```

- A function that you introduce with `async def` is a coroutine. It may use `await`, `return`, or `yield`, but all of these are optional.
- Just like it’s a `SyntaxError` to use `yield` outside of a `def` function, it is a `SyntaxError` to use `await` outside of an `async def` coroutine. You can only use `await` in the body of coroutines.

```python
async def f(x):
    y = await z(x)  # OK - `await` and `return` allowed in coroutines
    return y

async def g(x):
    yield x  # OK - this is an async generator

async def m(x):
    yield from gen(x)  # No - SyntaxError

def m(x):
    y = await z(x)  # Still no - SyntaxError (no `async def` here)
    return y
```

When you use `await f()`, it’s required that `f()` be an object that is awaitable.
An **awaitable** object is either.

1. Another coroutine
2. An object defining an `.__await__()` dunder method that returns an iterator.

Below two coroutines are essentially equivalent (both are awaitable), but the first is **generator-based**, while the second is a **native coroutine**:

```python
import asyncio

@asyncio.coroutine
def py34_coro():
    """Generator-based coroutine, older syntax and deprecated from python 3.10"""
    yield from stuff()

async def py35_coro():
    """Native coroutine, modern syntax with new features"""
    await stuff()
```

Another example

```python
import asyncio
import random

c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
    return i

async def main():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res

if __name__ == "__main__":
    random.seed(50)
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")
```

```bash
Initiated makerandom(0).
makerandom(0) == 2 too low; retrying.
makerandom(1) == 7 too low; retrying.
Initiated makerandom(2).
makerandom(2) == 7 too low; retrying.
makerandom(0) == 2 too low; retrying.
makerandom(1) == 6 too low; retrying.
makerandom(0) == 5 too low; retrying.
makerandom(0) == 0 too low; retrying.
---> Finished: makerandom(1) == 10
---> Finished: makerandom(0) == 10
makerandom(2) == 3 too low; retrying.
makerandom(2) == 5 too low; retrying.
makerandom(2) == 5 too low; retrying.
makerandom(2) == 5 too low; retrying.
---> Finished: makerandom(2) == 10

r1: 10, r2: 10, r3: 10
```

This program uses one main coroutine, `makerandom()`, and runs it concurrently across 3 different inputs.

## Async IO Design Patterns

### Chaining Coroutines

A key feature of coroutines is that they can be chained together. (Remember, a coroutine object is awaitable, so another coroutine can await it.)

```python
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
```

```bash
first(1) sleeping for 2 seconds.
first(2) sleeping for 7 seconds.
first(3) sleeping for 7 seconds.

Returning first(1)
second(1) sleeping for 2 seconds.
Returning second(1)

-->Chained: 1 => first-1 => second-first-1 (took 4.16 seconds).


Returning first(3)
second(3) sleeping for 6 seconds.

Returning first(2)
second(2) sleeping for 5 seconds.
Returning second(2)

-->Chained: 2 => first-2 => second-first-2 (took 12.05 seconds).

Returning second(3)

-->Chained: 3 => first-3 => second-first-3 (took 13.02 seconds).

Program finished in 13.03 seconds.
```

In this setup, the runtime of `main()` will be equal to the maximum runtime of the tasks that it gathers together and schedules.

### Using a Queue

A number of producers, which are not associated with each other, add items to a queue. Each producer may add multiple items to the queue at staggered, random, unannounced times. A group of consumers pull items from the queue as they show up, greedily and without waiting for any other signal.

In this design, there is no chaining of any individual consumer to a producer. The consumers don’t know the number of producers, or even the cumulative number of items that will be added to the queue, in advance.

The synchronous version of this program would look pretty dismal: a group of blocking producers serially add items to the queue, one producer at a time. Only after all producers are done can the queue be processed, by one consumer at a time processing item-by-item. There is a ton of latency in this design. Items may sit idly in the queue rather than be picked up and processed immediately.

The challenging part of this workflow is that there needs to be a signal to the consumers that production is done. Otherwise, `await q.get()` will hang indefinitely, because the queue will have been fully processed, but consumers won’t have any idea that production is complete.

```python
import asyncio
import itertools
import time
import os
import random


async def makeitem(size: int = 5) -> str:
    ''' return a hex string of 'size' bytes '''
    return os.urandom(size).hex()

async def randsleep(caller=None) -> None:
    ''' make caller sleep for random seconds ''' 
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} second")
    await asyncio.sleep(i)

async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in itertools.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")

async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()

async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    random.seed(100)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
```

```bash
$ python.exe .\asyncq.py -p 2 -c 10
Producer 0 sleeping for 4 second
Consumer 0 sleeping for 4 second
Consumer 1 sleeping for 7 second
Consumer 2 sleeping for 4 second
Consumer 3 sleeping for 4 second
Consumer 4 sleeping for 8 second
Consumer 5 sleeping for 10 second
Consumer 6 sleeping for 7 second
Consumer 7 sleeping for 8 second
Consumer 8 sleeping for 4 second
Consumer 9 sleeping for 7 second
Producer 0 added <0b9807dd12> to queue.
Producer 0 sleeping for 1 second
Consumer 0 got element <0b9807dd12> in 0.00363 seconds.    
Consumer 0 sleeping for 6 second
Producer 0 added <d67f8f6be5> to queue.
Producer 0 sleeping for 9 second
Consumer 2 got element <d67f8f6be5> in 0.00310 seconds.    
Consumer 2 sleeping for 3 second
Producer 0 added <58399ec238> to queue.
Producer 0 sleeping for 9 second
Consumer 3 got element <58399ec238> in 0.00355 seconds.    
Consumer 3 sleeping for 7 second
Producer 0 added <9f817e84e4> to queue.
Consumer 8 got element <9f817e84e4> in 0.00152 seconds.
Consumer 8 sleeping for 10 second
Program completed in 23.01225 seconds.
```

A producer puts anywhere from 1 to 5 items into the queue. Each item is a tuple of (i, t) where i is a random string and t is the time at which the producer attempts to put the tuple into the queue. When a consumer pulls an item out, it simply calculates the elapsed time that the item sat in the queue.

In this case, the items process in fractions of a second. A delay can be due to two reasons:

- Standard, largely unavoidable overhead
- Situations where all consumers are sleeping when an item appears in the queue

#### Notes

- `Task` an asyncio construct that tracks execution of a coroutine in a concrete event loop.
- `asyncio.create_task` submit a coroutine for execution and receive back a handle. You can await this handle when you actually need the result, or you can never await it, if you don't care about the result. This handle is the task, and it inherits from `Future`.
- `asyncio.gather` is **not the only way** to achieve concurrency in `asyncio`. It's just a utility function that makes it easier to wait for a number of coroutines to all complete, and submit them to the event loop at the same time. `create_task` does just the submitting.

## Async IO’s Roots in Generators

The use of `await` is a signal that marks a break point. It lets a coroutine temporarily suspend execution and permits the program to come back to it later.

### The fundamental difference between functions and generators

A function is all-or-nothing. Once it starts, it won’t stop until it hits a return, then pushes that value to the caller (the function that calls it). A generator, on the other hand, pauses each time it hits a `yield` and goes no further. Not only can it push this value to calling stack, but it can keep a hold of its local variables when you resume it by calling `next()` on it.

## The Event Loop and `asyncio.run()`

You can think of an event loop as something like a `while True` loop that monitors coroutines, taking feedback on what’s idle, and looking around for things that can be executed in the meantime. It is able to wake up an idle coroutine when whatever that coroutine is waiting on becomes available.

The entire management of the event loop has been implicitly handled by one function call:

```python
asyncio.run(main())  # Python 3.7+
```

`asyncio.run()`, introduced in Python 3.7, is responsible for getting the event loop, running tasks until they are marked as complete, and then closing the event loop.

1. Coroutines don’t do much on their own until they are tied to the event loop. If you have a main coroutine that awaits others, simply calling it in isolation has little effect:

    ```python
    import asyncio

    async def main():
        print("Hello")
        await asyncio.sleep(1)
        print("World")

    routine = main()
    routine
    ```

    Remember to use asyncio.run() to actually force execution by scheduling the main() coroutine (future object) for execution on the event loop:

    ```python
    >>> asyncio.run(routine)
    Hello ...
    World!
    ```

    (Other coroutines can be executed with `await`. It is typical to wrap just `main()` in `asyncio.run()`, and chained coroutines with await will be called from there.)

2. By default, an async IO event loop runs in a single thread and on a single CPU core. Usually, running one single-threaded event loop in one CPU core is more than sufficient. It is also possible to run event loops across multiple cores but not stable though.

3. Event loops are pluggable. That is, you could, if you really wanted, write your own event loop implementation and have it run tasks just the same. That is what is meant by the term “pluggable event loop”: you can use any working implementation of an event loop, unrelated to the structure of the coroutines themselves.

## Async IO in Context

1. Simply putting async before every function is a bad idea if all of the functions use blocking calls. (This can actually slow down your code.). Like `sockets` or `time.sleep`.
2. Threading also tends to scale less elegantly than async IO, because threads are a system resource with a finite availability. Creating thousands of threads will fail on many machines. Creating thousands of async IO tasks is completely feasible.
3. Async code do not create thread at background. Everything happend in just one thread (Event Loop) as we rapidly alternated the functions/coroutines which are waiting (awaited) for some result will be suspended and the one who are ready will be executed in current Event Loop. This save us from compelication of multi threading and multiprocessing. The `await` line in a coroutine hand over the controlls from coroutine executing to the event loop which can then execute the next productive coroutine.
4. The biggest reason not to use it is that await only supports a specific set of objects that define a specific set of methods. If you want to do async read operations with a certain DBMS, you’ll need to find not just a Python wrapper for that DBMS, but one that supports the async/await syntax. Coroutines that contain synchronous calls block other coroutines and tasks from running.

## Other Top-Level asyncio Functions

### `create_task()`

You can use `create_task()` to schedule the execution of a coroutine object, followed by `asyncio.run()`:

```python
import asyncio

async def coroutine(lst):
    ''' IO wait time is proportional to max element in list '''
    await asyncio.sleep(max(lst))
    return list(reversed(lst))


async def main():
    lst = [1, 2, 3]
    task = asyncio.create_task(coroutine(lst))
    # await let asyncio.run(main()) know about all the coroutines
    # included in the main() coroutines, basically a linking bw main 
    # and sub coroutines
    result = await task

    print("result : ", result) 
    print("Type : ", type(task)) 
    print("Done : ", task.done())

t = asyncio.run(main())
```

```bash
result :  [3, 2, 1]
Type :  <class '_asyncio.Task'>
Done :  True
```

Lets see what happens when we remove await from task

```python
import asyncio

async def coroutine(lst):
    ''' IO wait time is proportional to max element in list '''
    await asyncio.sleep(max(lst))
    return list(reversed(lst))


async def main():
    lst = [1, 2, 3]
    task = asyncio.create_task(coroutine(lst))
    # result = await task

    # print("result : ", result) 
    print("Type : ", type(task))
    print("Done : ", task.done())

t = asyncio.run(main())
```

```bash
Type :  <class '_asyncio.Task'>
Done :  False
```

The coroutine `main()` gets completed successfully without fail/error but since the `task` coroutine/task was not coupled/awaited then `main()` gets finished without waiting for `task` to get completed. But in case `main()` wait for some other reason then we see `create_task()` had already put the coroutine in event loop and it gets executed after some time as we see Done as True.

```python
import asyncio

async def coroutine(lst):
    ''' IO wait time is proportional to max element in list '''
    return list(reversed(lst))


async def main():
    lst = [1, 2, 3]
    task = asyncio.create_task(coroutine(lst))

    await asyncio.sleep(1)
    print("Type : ", type(task))
    print("Done : ", task.done())

t = asyncio.run(main())
```

```bash
Type :  <class '_asyncio.Task'>
Done :  True
```

Because `asyncio.run(main())` calls `loop.run_until_complete(main())`, the event loop is only concerned (without `await t` present) that `main()` is done, not that the tasks that get created within `main()` are done. Without `await t`, the loop’s other tasks will be cancelled, possibly before they are completed. If you need to get a list of currently pending tasks, you can use `asyncio.Task.all_tasks()`.

### gather()

`gather()` is meant to neatly put a collection of coroutines (futures) into a single future. As a result, it returns a single future object, and, if you `await asyncio.gather()` and specify multiple tasks or coroutines, you’re waiting for all of them to be completed. (This somewhat parallels `queue.join()` from our earlier example.) The result of `gather()` will be a list of the results across the inputs:

```python
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
```

```bash
Both tasks done: True
Time taken: 1.00492 seconds
[[1, -1, -3], [1, 0, -1]]
```

Noticed that `gather()` waits on the entire result set of the Futures or coroutines that you pass it. Alternatively, you can loop over `asyncio.as_completed()` to get tasks as they are completed, in the order of completion.
