#!/usr/bin/env python3
from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text("utf-8")


setup(
    name="sofapal",
    version="0.0.9",
    description="A modular command-line interface with AI function calling",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/slumberdemon/pal",
    author="SlumberDemon",
    author_email="hi@sofa.sh",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(where="."),
    install_requires=[
        "inquirerpy",
        "pytermgui",
    ],
    package_dir={"": "."},
    package_data={
        "pal": ["plugins/*.py"],
    },
    entry_points={
        "console_scripts": [
            "pal=pal.main:run",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/slumberdemon/pal/issues",
        "Source": "https://github.com/slumberdemon/pal",
    },
)
