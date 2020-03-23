"""
A JSON builder to create a users.json file for CTFd
"""

from autoctfd.templates.user import User

from autoctfd.templates.ctfdjson import CTFdJSON


def build_users(*users: User) -> CTFdJSON:
    """
    Build a users.json contents with supplied Users
    """

    json = CTFdJSON(users)
    return json
