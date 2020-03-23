#!/usr/bin/env python3

import os
import argparse
import readline
import getpass
import tempfile
import zipfile
import json
from pprint import pprint
import shutil
import configparser
from colorama import *

import autoctfd.output as output

from autoctfd.templates.rawjson import JSON
from autoctfd.templates.config import Config
from autoctfd.templates.user import User

from autoctfd.builders.users import build_users
from autoctfd.builders.pages import build_pages
from autoctfd.builders.config import build_config

from autoctfd.generators.challenges import generate_challenges


argparser = argparse.ArgumentParser(
    description="Create a CTFd importable database out of predefined challenges"
)

argparser.add_argument(
    "--config", "-c", type=str, required=True, help="a .ini config file for ctf detail"
)
argparser.add_argument(
    "--output",
    "-o",
    type=str,
    required=True,
    help="a .zip output for the generated ctfd data",
)

args = argparser.parse_args()


if not os.path.exists(args.config):
    output.fatal_error(
        f"config file {Fore.YELLOW}{Style.BRIGHT}'{args.config}'{Fore.RESET}{Style.RESET_ALL} does not exist!"
    )

config = configparser.ConfigParser()
try:
    config.read(args.config)

except configparser.MissingSectionHeaderError:
    output.fatal_error(
        f"no section headers in {Fore.YELLOW}{Style.BRIGHT}'{args.config}'{Fore.RESET}{Style.RESET_ALL}!"
    )

if "ctf" not in config.sections():
    output.fatal_error(
        f"no 'ctf' section in {Fore.YELLOW}{Style.BRIGHT}'{args.config}'{Fore.RESET}{Style.RESET_ALL}!"
    )

"""
This are the required configuration settings in the user supplied config file.
"""
required_configs = [
    "name",
    "description",
    "admin",
    "password",
    "email",
]

for required in required_configs:
    if required not in config["ctf"]:
        output.error(f"no '{required}' setting in'{args.config}'!")
    else:
        output.success(
            f"loaded ctf config {Fore.CYAN}{Style.BRIGHT}{required}{Fore.RESET}{Style.RESET_ALL}: {Fore.GREEN}{Style.BRIGHT}{config['ctf'][required]}{Fore.RESET}{Style.RESET_ALL}"
        )

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


RECREATE_JSON = {
    "config.json": build_config(
        Config(config["ctf"]["name"], config["ctf"]["description"])
    ),
    "pages.json": build_pages(),
    "users.json": build_users(
        User(
            config["ctf"]["admin"],
            config["ctf"]["password"],
            config["ctf"]["email"],
            admin=True,
            hidden=True,
        )
    ),
}


def build_zip():
    output.info("beginning to bundle CTFd zip file")

    with tempfile.TemporaryDirectory() as ctfd_dir:
        output.info(f"creating temporary directory {Fore.CYAN}{ctfd_dir}{Fore.RESET}")

        # Create each necessary directory
        for directory in NECESSARY_DIRS:
            output.info(f"creating inner directory {Fore.CYAN}{directory}{Fore.RESET}")

            ctfd_inner_dir = os.path.join(ctfd_dir, directory)
            if directory == "db":
                ctfd_db_dir = ctfd_inner_dir

            if directory == "uploads":
                ctfd_uploads_dir = ctfd_inner_dir

            os.mkdir(ctfd_inner_dir)

        # Now stage in all the challenges files.
        ChallengesJSON, FilesJSON, FlagsJSON = generate_challenges(ctfd_uploads_dir)

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
                            if file not in NECESSARY_JSON:
                                output.info(
                                    f"copying {Fore.MAGENTA}{new_json}{Fore.RESET}"
                                )
                            else:
                                output.info(
                                    f"templating {Fore.MAGENTA}{new_json}{Fore.RESET}"
                                )

                            ctfd_zip.write(new_json)
                        else:
                            # Use the regenerated file
                            with open(new_json, "w") as handle:
                                output.info(
                                    f"building {Fore.MAGENTA}{Style.BRIGHT}{new_json}{Style.RESET_ALL}{Fore.RESET}"
                                )
                                data = RECREATE_JSON[file]
                                if data is not None:
                                    handle.write(repr(data))
                                else:
                                    handle.write("")

                            ctfd_zip.write(new_json)
        output.success(
            f"created {Fore.GREEN}{Style.BRIGHT}{FINAL_ZIPFILE_NAME}{Fore.RESET}{Style.RESET_ALL}"
        )

        # Switch back to our directory for safety
        os.chdir(CURRENT_DIR)


build_zip()
