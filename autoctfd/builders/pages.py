"""
A JSON builder to create a users.json file for CTFd
"""

import glob
import os


from autoctfd.templates.pages import Page

from autoctfd.templates.rawjson import JSON


def build_pages():
    """
    Build pages.json contents
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
