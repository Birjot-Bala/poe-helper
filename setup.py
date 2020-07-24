from setuptools import setup

with open('requirements.txt', "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="poe_helper",
    version="0.1.dev",
    author="Birjot Bala",
    description="Look up items on POE Trade API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Birjot-Bala/poe-helper",
    packages=["poe_helper"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>3.6',
)