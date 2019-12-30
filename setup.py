#!/usr/bin/env python

"""The setup script."""

import os

from setuptools import find_packages, setup

__version__ = None

install_requires = []


def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)

    return open(file=path, mode=mode, encoding=encoding)


with open_local(["chatovod", "__version__.py"]) as f:
    exec(f.read())

with open_local(["README.rst"]) as f:
    long_description = f.read()

with open_local(["requirements.txt"]) as f:
    install_requires = f.readlines()

with open_local(["requirements-dev.txt"]) as f:
    dev_require = f.readlines()

with open_local(["requirements-test.txt"]) as f:
    tests_require = f.readlines()


extras_require = {
    "dev": dev_require + tests_require,
    "test": tests_require,
}

setup(
    author="Henrique Torres",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Chatovod Python library for bot lovers.",
    install_requires=install_requires,
    extras_require=extras_require,
    license="Apache Software License 2.0",
    long_description=long_description,
    include_package_data=True,
    keywords="chatovod.py",
    name="chatovod.py",
    packages=find_packages(include=["chatovod"]),
    test_suite="tests",
    url="https://github.com/Henriquetf/chatovod.py",
    version=__version__,
    zip_safe=False,
)
