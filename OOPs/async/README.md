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
    """Generator-based coroutine, older syntax"""
    yield from stuff()

async def py35_coro():
    """Native coroutine, modern syntax"""
    await stuff()
```
