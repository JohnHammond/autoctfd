"""
A CTFd tracking element.

This class is necessary to not break the server and keep at least one IP 
address known to CTFd.

"""

import time
import datetime

from autoctfd.jsonskeleton import JSON


class Tracking(JSON):
    def __init__(self):

        """
        This constructors creates class properties for each element that
        should be necessary in the CTFd JSON format.
        """

        self.type = None
        self.ip = None
        self.user_id = None
        self.date = datetime.datetime.utcfromtimestamp(time.time()).isoformat()
