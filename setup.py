from setuptools import setup, find_packages

setup(
    name="brick_sequencer",
    version="0.1a",
    packages=find_packages(),

    entry_points={
        "console_scripts": [
            "brick_sequencer = brick_sequencer.__main__:main",
            "brick-convert = brick_sequencer.image:main",
        ]
    },
)
