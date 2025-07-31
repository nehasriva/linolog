#!/usr/bin/env python3
"""
LinoLog - Linocut Print Metadata Logger
Setup script for package installation
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="linolog",
    version="1.0.0",
    author="LinoLog Contributors",
    author_email="your-email@example.com",
    description="A lightweight, Python-based, agent-assisted logging system for linocut prints",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/linolog",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/linolog/issues",
        "Source": "https://github.com/yourusername/linolog",
        "Documentation": "https://github.com/yourusername/linolog/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "linolog=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="linocut, printmaking, metadata, logging, google-sheets, ai-agents",
) 