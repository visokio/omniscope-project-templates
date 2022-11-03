#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mustafa
"""


index_file_name = "index.json"

# a new index.json is created for all individual templates
supported_versions = [1]

# the script will raise an error if these keys are not found in the individual template index.json.
keys_required = ["name", "version", "actions", "pinBlocks"]

import os
import json


def checkFileExists(filePath:str): 
 if not os.path.isfile(filePath):
            raise Exception(f"This file is missing {filePath}")




def process_directory(path: str, templates):
    with open(path+"/index.json", 'r') as index_file:
        manifest = json.load(index_file)

        if not "version" in manifest or not manifest["version"] in supported_versions:
            return

        # This is a template project folder....
        checkFileExists(path + "/thumbnail.png");
        checkFileExists(path + "/template.ioz");
        checkFileExists(path + "/README.md");

        for key in keys_required:
            if not key in manifest or manifest[key] is None:
                raise Exception(f"Key {key} is required but not present in manifest {path}/index.json")

        folder = os.sep.join(path.split(os.sep)[1:])
        
        aTemplate = {}

        for manifestKey in manifest: 
            aTemplate[manifestKey] = manifest[manifestKey]

        # This is used by the server side to ensure we know the project the user is trying to create a 
        # template from.
        aTemplate["path"] = folder
        templates.append(aTemplate)



templates = []
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    for file in files:
        if file == "index.json":
            process_directory(root, templates)


with open(index_file_name, 'w') as index_file:
    json.dump({"templates": templates}, index_file, indent=4)
