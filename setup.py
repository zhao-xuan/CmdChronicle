#!/usr/bin/env python3
"""
Setup script for CmdChronicle
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="cmdchronicle",
    version="1.0.0",
    author="CmdChronicle Team",
    author_email="",
    description="A command-line tool that analyzes your command history to discover patterns and generate insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cmdchronicle",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cmdchronicle=cmdchronicle:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="command-line, history, analysis, automation, productivity, shell",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cmdchronicle/issues",
        "Source": "https://github.com/yourusername/cmdchronicle",
        "Documentation": "https://github.com/yourusername/cmdchronicle#readme",
    },
) 