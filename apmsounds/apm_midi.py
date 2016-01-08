import warnings
import asyncio

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import mido

"""
Tablatura quadre de codis midi amb notes
http://computermusicresource.com/midikeys.html

Install extra
libportmidi-dev
"""

# Config if you just want to enqueue the sounds or play them at the same time
SINGLE_SOUND_AT_SAME_TIME = True

QUEUE = asyncio.Queue()

FIRST_KEY = 36
NUMBER_KEYS = 61
LAST_NOTE = FIRST_KEY + NUMBER_KEYS - 1

KEY_MAPPING = {}
FILENAME = "sound_list.txt"
FILE_LOCATION="/home/paurullan/Dropbox/sons-apm/ogg/{}.ogg"

with open(FILENAME) as f:
    for key, filename in enumerate(f.readlines(), FIRST_KEY):
        KEY_MAPPING[key] = filename.strip()

if len(KEY_MAPPING) > NUMBER_KEYS:
    warnings.warn("There are more files than notes;"
                  " many files will not be accesible")
else:
    log.debug("Loaded sounds: %d" % len(KEY_MAPPING))

def process_keystroke(message):
    if message.type != 'note_on':
        return
    if message.velocity <= 0:
        return
    key = message.note
    filename = KEY_MAPPING.get(key)
    if filename:
        QUEUE.put_nowait(filename)
        log.debug("enqueued %d | %s" % (QUEUE.qsize(), filename))
    else:
        log.debug("No file mapped for this key: %d" % key)

async def infinite_append():
    while True:
        await asyncio.sleep(.1)

async def consume():
    filename = await QUEUE.get()
    log.debug("pending  %d | %s" % (QUEUE.qsize(), filename))
    _exec = " ".join(["mpv -really-quiet", FILE_LOCATION.format(filename), ])
    process = await asyncio.create_subprocess_shell(_exec)
    if SINGLE_SOUND_AT_SAME_TIME:
        await process.wait()

async def consumer():
    while True:
        await consume()


# http://mido.readthedocs.org/en/latest/ports.html
names = mido.get_input_names()
midi_names = [n for n in names if "MIDI" in n]
if not midi_names:
	raise ConnectionError("Could not find MIDI controller")
name = midi_names[0]
inport = mido.open_input(name)
inport.callback = process_keystroke


loop = asyncio.get_event_loop()
tasks = [
    asyncio.Task(infinite_append()),
    asyncio.Task(consumer()),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
