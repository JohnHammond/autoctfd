"""
A CTFd user.

This class is primary used to generate the admin account

"""

import time
import datetime

from passlib.hash import bcrypt_sha256
from autoctfd.jsonskeleton import JSON


class User(JSON):
    def __init__(self, name, password, email, admin=False, hidden=False):

        """
        This constructors creates class properties for each element that
        should be necessary in the CTFd JSON format.
        """

        self.oauth_id = None
        self.name = name
        self.password = bcrypt_sha256.hash(str(password))
        self.email = email
        self.type = "admin" if admin else "user"
        self.website = None
        self.affiliation = None
        self.country = None
        self.bracket = None
        self.secret = None
        self.hidden = True if hidden else False
        self.banned = False
        self.verified = True
        self.team_id = True
        self.created = datetime.datetime.utcfromtimestamp(time.time()).isoformat()
