from setuptools import setup

import phisherman

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="phisherman.py",
    author=phisherman.__author__,
    author_email="example@gmail.com",
    version=phisherman.__version__,
    long_description=desc,
    long_description_content_type="text/markdown",
    license=phisherman.__license__,
    url=phisherman.__github__,
    packages=["phisherman"],
    download_url="https://github.com/QristaLabs/phisherman.py/archive/refs/tags/v0.1.1.tar.gz",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    exclude=("__pycache__"),
    install_requires=["aiohttp"]
)
