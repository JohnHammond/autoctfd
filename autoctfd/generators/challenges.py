"""
Builder functions for CTFd JSON
"""

import glob
import os
import subprocess
import json
import hashlib
import shutil

from autoctfd.templates.rawjson import JSON
from autoctfd.output import *


def generate_challenges(ctfd_upload_path: str):
    """
    TO-DO: Build challenges file 
    """

    def is_executable(fpath) -> bool:
        return os.access(fpath, os.X_OK)

    def md5sum(path) -> str:
        """
        Quick convenience function to get the MD5 hash of a file.
        """
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)

        return md5.hexdigest()

    # Prepare the Challenges JSON to be created
    ChallengesJSON = JSON()
    ChallengesJSON.results = []
    ChallengesJSON.meta = {}

    # Prepare the Files JSON to be created
    FilesJSON = JSON()
    FilesJSON.results = []
    FilesJSON.meta = {}

    # Prepare the Flags JSON to be created
    FlagsJSON = JSON()
    FlagsJSON.results = []
    FlagsJSON.meta = {}

    # Define some variables that are used in this process
    generate_scripts = ["./generate.py", "./generate.sh"]
    challenge_json_filename = "challenge.json"
    flag_filename = "flag.txt"

    current_directory = os.getcwd()

    challenges = glob.glob("challenges/*")

    for chal in challenges:

        if os.path.isdir(chal):
            os.chdir(chal)

            generate_script = None
            for genscript in generate_scripts:
                if os.path.exists(genscript):
                    generate_script = genscript
                    break

            # If we found a generate script...
            if generate_script is not None:
                # If the generate script is executable, run it!
                if is_executable(generate_script):
                    info(f"generating {Fore.YELLOW}{chal}{Fore.RESET}")

                    p = subprocess.Popen(
                        generate_script,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    p.wait()

            if os.path.exists(challenge_json_filename):

                challenge_json = json.load(open(challenge_json_filename))

                files = challenge_json.pop("_files")
                challenge_json["id"] = len(ChallengesJSON.results) + 1
                ChallengesJSON.results.append(challenge_json)

            for each_file in files:

                # Determine the upload path for this file
                upload_path = os.path.join(md5sum(each_file), each_file)
                full_upload_path = os.path.join(ctfd_upload_path, upload_path)
                full_upload_dir = os.path.dirname(full_upload_path)

                # Make the upload directory for this file
                os.mkdir(full_upload_dir)

                # Copy the file to the upload directory
                shutil.copy(each_file, full_upload_path)

                # Create the JSON for the file
                FilesJSON.results.append(
                    {
                        "id": len(FilesJSON.results) + 1,
                        "type": "challenge",
                        "location": upload_path,
                        "challenge_id": challenge_json["id"],
                        "page_id": None,
                    }
                )

            if os.path.exists(flag_filename):

                # Read the file
                with open(flag_filename, "r") as flag_handle:
                    flag = flag_handle.read().strip()

                # Create the JSON for the flag file
                FlagsJSON.results.append(
                    {
                        "id": len(FlagsJSON.results) + 1,
                        "challenge_id": challenge_json["id"],
                        "type": "static",
                        "content": flag,
                        "data": "case_insensitive",
                    }
                )

        # Switch back to the top-level directory before other challs
        os.chdir(current_directory)

    # Correct the count of each of the JSON files
    ChallengesJSON.count = len(ChallengesJSON.results)
    FlagsJSON.count = len(FlagsJSON.results)
    FilesJSON.count = len(FilesJSON.results)

    return ChallengesJSON, FilesJSON, FlagsJSON
