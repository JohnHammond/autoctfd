"""
Builder functions for CTFd JSON


"""

import glob
import os


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
    new_tracking.ip = "172.17.0.1"
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


def build_challenges():
    """
    TO-DO: Build challenges file 
    """

    pass


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
