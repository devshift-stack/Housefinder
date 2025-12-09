"""
Setup script for Housefinder
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="housefinder",
    version="4.0.0",
    author="Step2Job Team",
    author_email="housing@step2job.com",
    description="Automated Monteur Accommodation Finder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devshift-stack/Housefinder",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "housefinder=src.main:main",
        ],
    },
)
