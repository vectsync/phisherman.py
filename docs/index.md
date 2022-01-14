<p>
<a href="https://pypi.org/project/phisherman.py">
    <img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/phisherman.py">
</a>

<a href="https://pypi.org/project/flake8/">
    <img height="20" alt="Flake badge" src="https://img.shields.io/badge/code%20style-flake8-blue.svg">
</a>

<a href="https://qristalabs.github.io/phisherman.py">
    <img height="20" alt="Documentation status" src="https://img.shields.io/badge/documentation-up-00FF00.svg">
</a>
</p>

**Source Code**: [github.com/QristaLabs/phisherman.py](https://github.com/QristaLabs/phisherman.py)<br>
**PyPi**: [pypi.org/project/phisherman.py](https://pypi.org/project/phisherman.py)

Phisherman.py is an async API wrapper made in Python for [Phisherman.gg](https://phisherman.gg) which is a centralised database and scam links and is mainly designed for Discord bots to check URLs for any phishing links

```Python
import asyncio
from phisherman import Client

app = Client(token="Your Token")

async def main():
    if await app.check_domain("internetbadguys.com"):
        print("Detected suspicious.")

    await app.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
