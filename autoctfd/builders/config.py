"""
A JSON builder to create a config.json file for CTFd
"""

from autoctfd.templates.config import Config

from autoctfd.templates.ctfdjson import CTFdJSON


def build_config(config: Config) -> CTFdJSON:
    """
    Build a config.json contents with supplied Config object
    """

    # The config template from AutoCTFd does need to massage the data
    ctfd_config = []

    # To do this, we loop through each parameter and set it as a key,value
    each_id = 1
    for key, value in vars(config).items():
        ctfd_config.append(
            {"id": each_id, "key": key, "value": value,}
        )
        each_id += 1

    json = CTFdJSON(ctfd_config)
    return json
