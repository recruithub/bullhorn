from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="bullhorn",
    version="0.0.1",
    author="lloydtao (Lewis Lloyd)",
    author_email="lewis@recruit-hub.com",
    description="Python wrapper for the Bullhorn REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/recruithub/bullhorn",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
