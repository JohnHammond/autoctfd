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
import shutil

from autoctfd.user import User
from autoctfd.config import Config
from autoctfd.jsonskeleton import JSON

import autoctfd.builders


argparser = argparse.ArgumentParser(
    description="Generate a CTFd out of predefined challenges"
)

argparser.add_argument("--name", "-n", type=str, required=True)
argparser.add_argument("--output", "-o", type=str, required=True)

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

BASE_JSON_DIR = "_json"

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FINAL_ZIPFILE_NAME = args.output.replace(".zip", "") + ".zip"
FINAL_ZIPFILE_PATH = os.path.join(CURRENT_DIR, FINAL_ZIPFILE_NAME)
NECESSARY_DIRS = ["db", "uploads"]


class Setup:
    def __init__(self):

        self.ctf_name = input("CTF Name: ")
        self.ctf_description = input("CTF description: ")

        self.admin_username = input("Administrator Username: ")
        self.admin_password = getpass.getpass("Administrator Password: ")
        self.admin_email = input("Administrator E-mail:  ")


setup = Setup()

RECREATE_JSON = {
    "config.json": autoctfd.builders.build_config(
        Config(setup.ctf_name, setup.ctf_description)
    ),
    "pages.json": autoctfd.builders.build_pages(),
    "users.json": autoctfd.builders.build_users(
        User(
            setup.admin_username,
            setup.admin_password,
            setup.admin_email,
            admin=True,
            hidden=True,
        )
    ),
}


def build_zip():

    with tempfile.TemporaryDirectory() as ctfd_dir:

        # Create each necessary directory
        for directory in NECESSARY_DIRS:
            ctfd_inner_dir = os.path.join(ctfd_dir, directory)
            if directory == "db":
                ctfd_db_dir = ctfd_inner_dir

            if directory == "uploads":
                ctfd_uploads_dir = ctfd_inner_dir

            os.mkdir(ctfd_inner_dir)

        # Now stage in all the challenges files.
        ChallengesJSON, FilesJSON, FlagsJSON = autoctfd.builders.build_challenges(
            ctfd_uploads_dir
        )

        RECREATE_JSON["challenges.json"] = ChallengesJSON
        RECREATE_JSON["files.json"] = FilesJSON
        RECREATE_JSON["flags.json"] = FlagsJSON

        # Copy all the other files into the directory
        for j in NECESSARY_JSON:
            original_path = os.path.join(BASE_JSON_DIR, j)
            shutil.copy(original_path, ctfd_db_dir)

        # Hop to the CTFd directory so the ZIP file has correct paths
        os.chdir(ctfd_dir)

        # Now put all of the directories in the ZIP file
        with zipfile.ZipFile(FINAL_ZIPFILE_PATH, "w") as ctfd_zip:
            for directory in NECESSARY_DIRS:

                # Recursively grab all the files
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        new_json = os.path.join(root, file)
                        if file not in RECREATE_JSON:
                            ctfd_zip.write(new_json)
                        else:
                            # Use the regenerated file
                            with open(new_json, "w") as handle:
                                data = RECREATE_JSON[file]
                                if data is not None:
                                    handle.write(repr(data))
                                else:
                                    handle.write("")

                            ctfd_zip.write(new_json)

        # Switch back to our directory for safety
        os.chdir(CURRENT_DIR)


build_zip()
