import datetime
from asyncio import Task
import asyncio

CURRENT_TIME = None

async def uptime():
    while True:
        global CURRENT_TIME
        CURRENT_TIME = datetime.datetime.now()
        print("updated current time {}".format(CURRENT_TIME))
        #yield from asyncio.sleep(.2)
        await asyncio.sleep(.2)

async def show_time():
    while True:
        global CURRENT_TIME
        print(CURRENT_TIME)
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
tasks = [
    Task(uptime()),
    Task(show_time()),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
