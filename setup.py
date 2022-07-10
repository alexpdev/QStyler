#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2021-current alexpdev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################
"""Setup for Qstyler package."""

import json
from setuptools import find_packages, setup


def load_info():
    """Extract information from package.json and README files."""
    info = json.load(open("package.json"))
    with open("README.md", "rt", encoding="utf-8") as readme:
        info["long_description"] = readme.read()
    return info


INFO = load_info()

setup(
    version=INFO["version"],
    description=INFO["description"],
    long_description=INFO["long_description"],
    url=INFO["url"],
    author=INFO["author"],
    author_email=INFO["email"],
    long_description_content_type=INFO["long_description_content_type"],
    project_urls={"Source Code": INFO["repository"]["url"]},
    license=INFO["license"],
    packages=find_packages(exclude=[".env", "tests"]),
    include_package_data=True,
    entry_points={"console_scripts": ["qstyler = QStyler.window:execute"]},
    install_requires=["PySide6"],
    setup_requires=["setuptools", "wheel", "build"],
)
