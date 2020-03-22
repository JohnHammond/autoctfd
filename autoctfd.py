#!/usr/bin/env python3

import os

import argparse
import readline
import getpass
from passlib.hash import bcrypt_sha256
import tempfile
import zipfile
import json
from pprint import pprint

from autoctfd.user import User
from autoctfd.jsonskeleton import JSON


argparser = argparse.ArgumentParser(
    description="Generate a CTFd out of predefined challenges"
)

argparser.add_argument("--name", "-n", type=str, required=True)

args = argparser.parse_args()


"""
These JSON files are necessary in the `db` directory of the CTFd ZIP.
"""
NECESSARY_JSON = [
    "alembic_version.json",
    "awards.json",
    "challenges.json",
    "config.json",
    "dynamic_challenge.json",
    "files.json",
    "flags.json",
    "hints.json",
    "notifications.json",
    "pages.json",
    "solves.json",
    "submissions.json",
    "tags.json",
    "teams.json",
    "tokens.json",
    "tracking.json",
    "unlocks.json",
    "users.json",
]

"""
These JSON files will need to be recreated dynamically.
"""
RECREATE_JSON = [
    "config.json",
    "challenges.json",
    "files.json",
    "flags.json",
    "pages.json",
    "users.json",
]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FINAL_ZIPFILE_NAME = "newfile.zip"
FINAL_ZIPFILE_PATH = os.path.join(CURRENT_DIR, FINAL_ZIPFILE_NAME)
NECESSARY_DIRS = ["db", "uploads"]


admin_user = User("Admin", "passwords", "admin@admin.com", admin=True, hidden=True)

"""
Build the users JSON file
"""
UserJSON = JSON()
UserJSON.meta = {}
UserJSON.results = [vars(admin_user)]
UserJSON.count = len(UserJSON.results)


def build_zip():

    with tempfile.TemporaryDirectory() as ctfd_dir:

        # Create each necessary directory
        for directory in NECESSARY_DIRS:
            ctfd_db_dir = os.path.join(ctfd_dir, directory)
            os.mkdir(ctfd_db_dir)

        # Hop to the CTFd directory so the ZIP file has correct paths
        os.chdir(ctfd_dir)

        # Now put all of the directories in the ZIP file
        with zipfile.ZipFile(FINAL_ZIPFILE_PATH, "w") as ctfd_zip:
            for directory in NECESSARY_DIRS:
                ctfd_zip.write(directory)

        # Switch back to our directory for safety
        os.chdir(CURRENT_DIR)
