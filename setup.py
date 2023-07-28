from bullhorn import __version__, __title__, __author__, __license__
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    version=__version__,
    name=__title__,
    author=__author__,
    license=__license__,
    author_email="lewis@recruit-hub.com",
    description="Python wrapper for the Bullhorn REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/recruithub/bullhorn",
    packages=find_packages(),
    install_requires=[
        "requests>=2,<3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
