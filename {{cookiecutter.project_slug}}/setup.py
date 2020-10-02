#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import io
import os

from setuptools import find_packages, setup


def read_pipfile(file: str) -> dict:
    """
    A very simple function that parses the [package] and
    [dev-package] sections of a Pipfile.
    :param file: the Pipfile to parse
    :return: a dictionary that contains the packages and their versions
    """
    flag = ''
    pattern = re.compile(r"([\w\-_]+)\s=\s\"(.*?)\"")
    packages = {}
    dev_packages = {}
    with open(file, 'r') as pipfile:
        for line in pipfile:
            line = line.strip()
            if line == '[packages]':
                flag = 'packages'
                continue
            if line == '[dev-packages]':
                flag = 'dev-packages'
                continue
            if line == '':
                flag = ''
            if flag == 'packages':
                package = pattern.match(line).group(1)
                version = pattern.match(line).group(2)
                packages[package] = version
            elif flag == 'dev-packages':
                package = pattern.match(line).group(1)
                version = pattern.match(line).group(2)
                dev_packages[package] = version

    return {'packages': packages,
            'dev-packages': dev_packages}


# Package meta-data.
NAME = "{{cookiecutter.project_slug}}"
DESCRIPTION = "{{cookiecutter.project_description}}"
HOMEPAGE = "https://{{cookiecutter.project_slug}}.github.io/"
REPOSITORY = "https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}"
DOWNLOAD = "https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}/archive/master.zip"
BUG_TRACKER = "https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}/issues"
DOCUMENTATION = "https://{{cookiecutter.project_slug}}.readthedocs.io/"
EMAIL = "{{cookiecutter.email}}"
AUTHOR = "{{cookiecutter.full_name}}"
README = "README.rst"
REQUIRES_PYTHON = ">={{cookiecutter.python_version}}"
VERSION = "{{cookiecutter.version}}"
LICENSE = "{{cookiecutter.license}}"

# Specify the packages that are required by this module.
packages = read_pipfile('Pipfile')
REQUIRED = [f"{key}{value}" if value != '*' else f"{key}" for key, value in packages['packages'].items()]

# Define packages that are optional.
EXTRAS = {
    'dev': [f"{key}{value}" if value != '*' else f"{key}" for key, value in packages['dev-packages'].items()]
    # 'test': ['coverage']
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, README), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/x-rst; charset=UTF-8',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=HOMEPAGE,
    download_url=DOWNLOAD,
    project_urls={
        "Bug Tracker": BUG_TRACKER,
        "Documentation": DOCUMENTATION,
        "Source Code": REPOSITORY,
    },
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    package_data={'{{cookiecutter.project_slug}}': ['Pipfile']},
    include_package_data=True,

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    license=LICENSE,
    test_suite='pytest',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py [command] support.
    cmdclass={},
)
