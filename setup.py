from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="poe_helper",
    version="0.1.dev",
    author="Birjot Bala",
    description="Look up items on the PoE Trade API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Birjot-Bala/poe-helper",
    packages=["poe_helper"],
    install_requires=[
        "requests",
        "Pillow"
    ],
    entry_points={
        "gui_scripts": [
            "poe_helper = poe_helper.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>3.6',
)