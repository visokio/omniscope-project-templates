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


def create_block_overview(f, blocks):
    f.write("## Template Overview\n")

    for category in sections:

        subcategories = list(sections[category].keys())
        subcategories.sort(key=cmp_to_key(compare))

        for subcategory in subcategories:

            for block in sections[category][subcategory]:

                f.write(f'<div id="{block["id"]}"/>\n\n')
                f.write(f'### {block["name"]}\n\n')

                has_thumbnail = "thumbnail" in block

                if has_thumbnail:
                    f.write(f'<img align="right" src="https://github.com/visokio/omniscope-custom-blocks/blob/master/{block["thumbnail"]}" width="125" height="125"/>\n\n')

                f.write(f'{block["description"]}\n\n')
                f.write(f'[Link to Github page]({block["relative_path"]})\n\n')







def process_directory(root_path: str, path_parts, blocks):
    with open(root_path+"/manifest.json", 'r') as manifest_file:
        manifest = json.load(manifest_file)

        if not "optionsVersion" in manifest or not manifest["optionsVersion"] in supported_options_versions:
            return

        relative_path = os.sep.join(path_parts)

        id = "".join(list(map(lambda s: s.replace(" ", ""), path_parts)))

        block = {}
        block["id"] = id
        block["path"] = root_path
        block["relative_path"] = urllib.parse.quote(relative_path)
        block["name"] = manifest["name"]
        block["language"] = manifest["language"]
        block["description"] = manifest["description"]
        block["category"] = manifest["category"]
        if "subcategory" in manifest and not manifest["subcategory"] is None:
            block["subcategory"] = manifest["subcategory"]

        if path.isfile(root_path+"/thumbnail.png"):
            block["thumbnail"] = relative_path+"/thumbnail.png"


        blocks.append(block)




blocks = []

for root, dirs, files in os.walk("."):
    root_path = root.split(os.sep)
    path_parts = root_path[1:]
    for file in files:
        if file == "manifest.json":
            process_directory(root, path_parts, blocks)



with open(readme_file_name, 'w') as readme_file:
    create_header(readme_file)
    #create_block_overview(readme_file, blocks)
