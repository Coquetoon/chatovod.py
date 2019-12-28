#!/usr/bin/env python

"""The setup script."""

from chatovod import __version__

from setuptools import find_packages, setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Henrique Torres",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Chatovod Python library for bot lovers.",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    include_package_data=True,
    keywords="chatovod.py",
    name="chatovod.py",
    packages=find_packages(include=["chatovod.py", "chatovod.py.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Henriquetf/chatovod.py",
    version=__version__,
    zip_safe=False,
)
