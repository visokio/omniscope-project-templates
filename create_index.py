#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mustafa
"""


index_file_name = "index.json"

# a new index.json is created for all individual templates
supported_versions = [1]

# the script will raise an error if these keys are not found in the individual template index.json.
keys_required = ["name", "version", "workflowActions", "pinBlocks"]

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

        if (os.path.basename(path) != manifest["name"]):
            raise Exception("Folder name and index.json name must match" + os.path.basename(path) + " != " + manifest["name"] + " for folder: " + path);

        for key in keys_required:
            if not key in manifest or manifest[key] is None:
                raise Exception(f"Key {key} is required but not present in {path}/index.json")

        folder = os.sep.join(path.split(os.sep)[1:])
        
        aTemplate = {}

        for manifestKey in manifest: 
            aTemplate[manifestKey] = manifest[manifestKey]

        templates.append(aTemplate)



templates = []
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    for file in files:
        if file == "index.json":
            process_directory(root, templates)


with open(index_file_name, 'w') as index_file:
    templateCategories = {

        "All": {
            "foregroundColour": "white",
            "backgroundColour": "#7a9cdf"
        },
        "General": {
            "foregroundColour": "white",
            "backgroundColour": "#6ac1d4"
        },
        "Social": {
            "foregroundColour": "white",
            "backgroundColour": "#cf8059"
        }

        
    }


    json.dump({ "categories": templateCategories, "templates": templates}, index_file, indent=4)
