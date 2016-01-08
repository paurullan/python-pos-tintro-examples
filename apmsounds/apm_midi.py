import warnings
import asyncio
import time

import mido

QUEUE = asyncio.Queue()

FIRST_KEY = 39
NUMBER_KEYS = 61
LAST_NOTE = FIRST_KEY + NUMBER_KEYS - 1

KEY_MAPPING = {}
FILENAME = "sound_list.txt"

with open(FILENAME) as f:
    for key, filename in enumerate(f.readlines(), FIRST_KEY):
        KEY_MAPPING[key] = filename

if len(KEY_MAPPING) > NUMBER_KEYS:
    warnings.warn("There are more files than notes;"
                  " many files will not be accesible")


def process_keystroke(message):
    if message.type != 'key_on':
        return
    if message.velocity <= 0:
        return
    key = message.note
    if not (FIRST_KEY < key < LAST_NOTE):
        raise ValueError("Found item")
    QUEUE.put_nowait(key)


# http://mido.readthedocs.org/en/latest/ports.html
device_names = mido.get_device_names()


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
    asyncio.Task(consumer()),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
