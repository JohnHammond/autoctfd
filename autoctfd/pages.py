"""
A CTFd page.

This class is used to generate pages accessible within the CTF.

"""

from autoctfd.jsonskeleton import JSON


class Page(JSON):
    def __init__(self):

        """
        This constructors creates class properties for each element that
        should be necessary in the CTFd JSON format.
        """

        self.title = None
        self.route = None
        self.content = None
        self.draft = False
        self.hidden = None
        self.auth_required = None
