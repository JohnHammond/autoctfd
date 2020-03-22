"""
Builder functions for CTFd JSON


"""

import glob
import os
import subprocess
import json
import hashlib
import shutil

from autoctfd.user import User
from autoctfd.pages import Page
from autoctfd.config import Config
from autoctfd.tracking import Tracking
from autoctfd.jsonskeleton import JSON


def build_users(*users: User) -> JSON:
    """
    Build a users.json contents with supplied Users
    """

    UserJSON = JSON()
    UserJSON.meta = {}

    UserJSON.results = []
    for user in users:
        UserJSON.results.append(vars(user))

    UserJSON.count = len(UserJSON.results)

    return UserJSON


def build_tracking() -> JSON:
    """
    Build a users.json contents with supplied Users
    """

    TrackingJSON = JSON()
    TrackingJSON.meta = {}

    TrackingJSON.results = []
    new_tracking = Tracking()
    new_tracking.id = len(TrackingJSON.results) + 1
    new_tracking.user_id = 1
    new_tracking.ip = "127.0.0.1"
    TrackingJSON.results.append(vars(new_tracking))

    TrackingJSON.count = len(TrackingJSON.results)

    return TrackingJSON


def build_config(config: Config) -> JSON:
    """
    Build a configuration file 
    """

    ConfigJSON = JSON()
    ConfigJSON.meta = {}

    ConfigJSON.results = []
    for key, value in vars(config).items():
        ConfigJSON.results.append(
            {"id": len(ConfigJSON.results) + 1, "key": key, "value": value,}
        )
    ConfigJSON.count = len(ConfigJSON.results)

    return ConfigJSON


def build_challenges(ctfd_upload_path: str):
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

    # print(ChallengesJSON)
    # print("")
    # print(FilesJSON)
    # print("")
    # print(FlagsJSON)


def build_files():
    """
    TO-DO: Build challenges file 
    """

    pass


def build_flags():
    """
    TO-DO: Build challenges file 
    """

    pass


def build_pages():
    """
    TO-DO: Build challenges file 
    """

    pages = glob.glob("pages/*.html")

    PageJSON = JSON()
    PageJSON.meta = {}

    PageJSON.results = []
    for p in pages:
        name = os.path.basename(p).replace(".html", "")

        new_page = Page()
        new_page.id = len(PageJSON.results) + 1
        new_page.title = name.title()
        new_page.route = name.lower()
        new_page.content = open(p, "r").read()
        PageJSON.results.append(vars(new_page))

    PageJSON.count = len(PageJSON.results)

    return PageJSON
