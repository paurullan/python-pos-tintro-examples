import aiohttp
import asyncio

import json

"""
Get how many closed issues there are at Twitter's bootstrap
"""

async def github_issues(repo):
    base_url = "https://api.github.com/repositories/{repo}/issues?state=closed"
    url = base_url.format(repo=repo)
    response = await aiohttp.request('GET', url)
    data_json = await response.text()
    data = json.loads(data_json)
    issues = len(data)
    return issues

if __name__ == '__main__':
    bootstrap = 2126244
    loop = asyncio.get_event_loop()
    issues = loop.run_until_complete(github_issues(repo=bootstrap))
    print(issues)
