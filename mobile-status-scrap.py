import random
import asyncio

async def check_site(country: str=None):
    if not str:
        country = "Somewhere"
    await asyncio.sleep(1 + random.random())
    print("Hello from {}".format(country))

if __name__ == "__main__":
    countries = ("ES", "ŀ", None, )
    loop = asyncio.get_event_loop()
    f = asyncio.wait(map(check_site, countries))
    loop.run_until_complete(f)
