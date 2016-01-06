import asyncio
import time

QUEUE = asyncio.Queue()

FILENAME = "/home/paurullan/Dropbox/sons-apm/ogg/pero_que_dius.ogg"

async def infinite_append():
    while True:
        await QUEUE.put((FILENAME, time.time()))
        await asyncio.sleep(.5)

async def consume():
    filename, when = await QUEUE.get()
    print(QUEUE.qsize())
    print("Recollit: {}".format(when))
    _exec = " ".join(["mpv -really-quiet", filename, ])
    process = await asyncio.create_subprocess_shell(_exec)
    await process.wait()

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
