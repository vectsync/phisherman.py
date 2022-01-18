<h1 align="center">Phisherman.py</h1>
<h3 align="center">
Asynchronous Python API Wrapper for phisherman.gg
</h3>

<!-- Badges. -->
<p align="center">
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

## Installation

**Python 3.8 or above is required**

```sh
# Stable
pip install phisherman.py

# Development
pip install git+https://github.com/QristaLabs/phisherman.py
```

## Example

```python
import asyncio
from phisherman import Client

app = Client(token="Your Token")

async def main():
    if await app.check_domain("internetbadguys.com"):
        print("Detected suspicious.")

    await app.close()

asyncio.run(main())
```

## Links

- [Documentation](https://qristalabs.github.io/phisherman.py)
- [Phisherman](https://phisherman.gg)
- [API Support Server](https://discord.gg/8sPG4m84Vb)
