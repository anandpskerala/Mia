import os
import glob
import logging
from os.path import dirname, basename, isfile

from mia import CONFIG


def _all_modules():
    """
    To get the list of all modules
    """
    not_modules = ["localization", "__init__.py", "__main__.py", "__pycache__"]
    paths = glob.glob(dirname(__file__) + "/*")
    all_modules = []
    for f in paths:
        if basename(f) in not_modules:
            continue
        elif isfile(f) and f.endswith(".py"):
            all_modules.append(basename(f)[:-3])
        else:
            all_modules.append(basename(f))

    if CONFIG.disabled_plugins:
        all_modules = list(
            filter(
                lambda m: m not in CONFIG.disabled_plugins,
                [item for item in all_modules]
            )
        )

    return sorted(all_modules)


MODULES = _all_modules()
