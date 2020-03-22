"""
An empty JSON class.

This class is easily handle JSON.

"""

import json
from passlib.hash import bcrypt_sha256
import time
import datetime


class JSON:
    def __init__(self):
        pass

    def __repr__(self):
        """
        This function will return the user in proper JSON form.
        """
        return json.dumps(vars(self))


"""
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "oauth_id": null,
      "name": "admin",
      "password": "$bcrypt-sha256$2b,12$7NIpGXGYrXD72MIAtWtt6.$x5zcXSQezsB9LHQMKGJlHisvARcbNQS",
      "email": "a@a.com",
      "type": "admin",
      "secret": null,
      "website": null,
      "affiliation": null,
      "country": null,
      "bracket": null,
      "hidden": true,
      "banned": false,
      "verified": false,
      "team_id": null,
      "created": "2020-03-22T01:28:29.044374"
    }
  ],
  "meta": {}
}
"""
