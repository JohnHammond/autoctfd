"""
All CTFd JSON elements match a certain pattern
"""

import json
from autoctfd.templates.rawjson import JSON


class CTFdJSON(JSON):
    def __init__(self, contents) -> JSON:
        """
        Build a CTFd json with given contents
        """

        self.rawjson = JSON()
        self.rawjson.meta = {}

        self.rawjson.results = []

        if type(contents) is tuple:
            for content in contents:
                self.rawjson.results.append(vars(content))
        elif type(contents) is list:
            for content in contents:
                self.rawjson.results.append(content)
        else:
            self.rawjson.results.append(vars(contents))

        self.rawjson.count = len(self.rawjson.results)

    def __repr__(self):
        """
        This function will return the user in proper JSON form.
        """
        self.rawjson.count = len(self.rawjson.results)
        return json.dumps(vars(self.rawjson))
