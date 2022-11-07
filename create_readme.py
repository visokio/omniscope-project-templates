#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mustafa
"""


readme_file_name = "README.md"

# a new index.json is created for all individual block manifests that have a supported optionsVersion
supported_options_versions = [1]


import os
import json
from os import path
import urllib.parse
from functools import cmp_to_key

def create_header(f):
    f.write("# Omniscope Project templates")
    f.write(" &middot; ")
    f.write("[![Refresh index](https://github.com/visokio/omniscope-project-templates/actions/workflows/refresh_index.yml/badge.svg)](https://github.com/visokio/omniscope-project-templates/actions/workflows/refresh_index.yml)")
    f.write("[![Refresh readme](https://github.com/visokio/omniscope-project-templates/actions/workflows/refresh_readme.yml/badge.svg)](https://github.com/visokio/omniscope-project-templates/actions/workflows/refresh_readme.yml)")
    f.write("\n\n")
    f.write("Public repository for project templates for Omniscope Evo.\n")
    f.write("\n")

def compare(a, b):

    if a is None:
        return 1
    if b is None:
        return -1

    if a > b: return 1
    elif a < b: return -1
    else: return 0


def create_template_overview(f, templates):
    f.write("## Template Overview\n")
    for aTemplate in templates:

        f.write(f'<div id="{aTemplate["id"]}"/>\n\n')
        f.write(f'### {aTemplate["name"]}\n\n')

        has_thumbnail = "thumbnail" in aTemplate

        if has_thumbnail:
            f.write(f'<img align="right" src="https://github.com/visokio/omniscope-project-templates/blob/master/{aTemplate["thumbnail"]}" width="125" height="125"/>\n\n')

        f.write(f'{aTemplate["description"]}\n\n')
        f.write(f'[Link to Github page]({aTemplate["relative_path"]})\n\n')


def process_directory(root_path: str, path_parts, templates):
    with open(root_path+"/index.json", 'r') as manifest_file:
        indexJson = json.load(manifest_file)

        if not "version" in indexJson or not indexJson["version"] in supported_options_versions:
            return

        relative_path = os.sep.join(path_parts)

        id = "".join(list(map(lambda s: s.replace(" ", ""), path_parts)))

        aTemplate = {}
        aTemplate["id"] = id
        aTemplate["path"] = root_path
        aTemplate["relative_path"] = urllib.parse.quote(relative_path)
        aTemplate["name"] = indexJson["name"]
        aTemplate["description"] = indexJson["description"]
        

        if path.isfile(root_path+"/thumbnail.png"):
            aTemplate["thumbnail"] = relative_path+"/thumbnail.png"

        templates.append(aTemplate)


templates = []

for root, dirs, files in os.walk("."):
    root_path = root.split(os.sep)
    path_parts = root_path[1:]
    for file in files:
        if file == "index.json":
            process_directory(root, path_parts, templates)



with open(readme_file_name, 'w') as readme_file:
    create_header(readme_file)
    create_template_overview(readme_file, templates)
