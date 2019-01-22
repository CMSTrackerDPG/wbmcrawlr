#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2018 CERN
#
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import open
from future import standard_library

standard_library.install_aliases()
import math
import os
import sys


def save_to_disk(path, content):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        print("Creating directory '{}'".format(directory))
        os.makedirs(directory)
    with open(path, "w") as file:
        file.write(content)


def flatten_run(run):
    run_flat = run["attributes"]
    for key, value in run["meta"]["row"].items():
        new_field_name = "{}_unit".format(key)
        run_flat.update({new_field_name: value["units"]})
    return run_flat


def progress_bar(current, total, text="", filler="#"):
    bar_length = 50
    processed = current / total
    processed_length = math.ceil(processed * bar_length)

    bar = filler * processed_length + "-" * (bar_length - processed_length)

    return "[{}] {:.2%} {}".format(bar, processed, text)


def print_progress(current, total, text):
    print(progress_bar(current, total, text), end="\r")
    sys.stdout.flush()
