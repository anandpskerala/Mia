import glob
import logging
from os.path import dirname, basename, isfile

from mia import CONFIG


def _all_modules():
    """
    To get the list of all modules
    """

    paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = sorted(
        [
            basename(f)[:-3] for f in paths if isfile(f) and f.endswith(".py") and not f.endswith('__init__.py') and
                                               not f.endswith('__main__.py')
        ]
    )

    if CONFIG.disabled_plugins:
        all_modules = list(
            filter(
                lambda m: m not in CONFIG.disabled_plugins,
                [item for item in all_modules]
            )
        )

    return all_modules


MODULES = _all_modules()
