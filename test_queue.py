import asyncio

QUEUE = asyncio.Queue()

async def infinite_append():
    while True:
        for i in range(4):
            print("put {}".format(i))
            await QUEUE.put(i)
        await asyncio.sleep(0.3)

async def consume():
    x = await QUEUE.get()
    print("Recollit: {}".format(x))

async def consumer():
    while True:
        await consume()

loop = asyncio.get_event_loop()
tasks = [
    asyncio.Task(infinite_append()),
    asyncio.Task(consumer()),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

