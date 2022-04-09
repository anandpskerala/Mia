import sys
import logging
import yaml
from typing import Optional, Set, List
from pydantic import BaseModel, ValidationError

from pyrogram import Client


class MiaConfig(BaseModel):
    """
    Config class
    """

    api_id: int
    api_hash: str
    bot_token: str
    database_url: str
    workers: Optional[int] = 4
    owner_id: int
    sudo_users: Set[int]
    whitelist_users: Set[int]
    work_dir: str
    disabled_plugins: List[str]
    prefixes: List[str]
    parse_mode: str
    default_lang: str


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)

logging.info("Checking for requirements to start Mia")

if sys.version_info < (3, 8, 0):
    logging.error(
        "Your Python version is too old for Mia to run, please update to Python 3.8 or above"
    )
    exit(1)


logging.info("Starting Mia...")

try:
    config_file = dict(
        yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader))
except Exception as error:
    logging.error(
        f"Could not load config file due to a {type(error).__name__}: {error}")
    exit(1)

try:
    CONFIG = MiaConfig(**config_file)
except ValidationError as validation_error:
    logging.error(
        f"Something went wrong when parsing config.yml: {validation_error}")
    exit(1)
CONFIG.sudo_users.add(CONFIG.owner_id)

"""
Pyrogram Client for the bot
"""

Mia = Client(
    "mia",
    api_id=CONFIG.api_id,
    api_hash=CONFIG.api_hash,
    bot_token=CONFIG.bot_token,
    workdir=CONFIG.work_dir,
    workers=200,
    parse_mode=CONFIG.parse_mode,
    plugins=dict(
        root="mia/modules",
        exclude=CONFIG.disabled_plugins
    )
)
