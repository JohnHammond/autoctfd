"""
An empty JSON class.

This class is easily handle JSON.

"""

import json
from passlib.hash import bcrypt_sha256
import time
import datetime


class JSON:
    def __repr__(self):
        """
        This function will return the user in proper JSON form.
        """
        return json.dumps(vars(self))
