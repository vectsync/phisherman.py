from setuptools import setup

import phisherman

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="phisherman",
    author=phisherman.__author__,
    author_email="example@gmail.com",
    version=phisherman.__version__,
    long_description=desc,
    long_description_content_type="text/markdown",
    license=phisherman.__license__,
    url=phisherman.__github__,
    packages=["phisherman"],
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
    install_requires=["aiohttp"],
)
