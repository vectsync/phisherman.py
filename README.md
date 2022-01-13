<h1 align="center">Phisherman.py</h1>
<p align="center">
<a href="https://pypi.org/project/phisherman.py"><img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/phisherman.py"></a>
<a href="https://pypi.org/project/black"><img height="20" alt="Black badge" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://qristalabs.github.io/phisherman.py"><img height="20" alt="Documentation status" src="https://img.shields.io/badge/documentation-up-00FF00.svg"></a>
</p>

<h4 align="center">Asynchronous Python API Wrapper for phisherman.gg</h4>


## Installation
**Python 3.8+ is required**

```sh
## Stable
pip install phisherman.py

## Development
pip install git+https://github.com/QristaLabs/phisherman.py
```

## Example
```Python
import asyncio
from phisherman import Application

app = Application(token="Your Token")

async def main():
    if await app.check_domain("internetbadguys.com"):
        print("Suspicious 0_o")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Links
[Documentation](https://qristalabs.github.io/phisherman.py)<br>
[Phisherman](https://phisherman.gg)<br>
[API Support Server](https://discord.gg/8sPG4m84Vb)
