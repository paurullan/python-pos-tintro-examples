import warnings
import asyncio
import threading

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

QUEUE = asyncio.Queue()
# mido uses callbacks AND threading so we cannot purely use asyncio
# and need to use an event to wake up the QUEUE
STUFF_IN_QUEUE = threading.Event()

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
        STUFF_IN_QUEUE.set()
        log.debug("enqueued %d | %s" % (QUEUE.qsize(), filename))
    else:
        log.debug("No file mapped for this key: %d" % key)

async def consume():
    STUFF_IN_QUEUE.wait()
    filename = await QUEUE.get()
    pendings = QUEUE.qsize()
    if not pendings:
        STUFF_IN_QUEUE.clear()
    log.debug("pending  %d | %s" % (pendings, filename))
    _exec = " ".join(["mpv -really-quiet", FILE_LOCATION.format(filename), ])
    process = await asyncio.create_subprocess_shell(_exec)
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
loop.create_task(consumer())
loop.run_forever()
