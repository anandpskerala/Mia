import os
import asyncio
import traceback
import logging

from pyrogram import idle
from mia import Mia, CONFIG
from .modules import MODULES


async def main():
    try:
        await Mia.start()
        logging.info("Loading Modules : %s", str(MODULES))
        logging.info("Not Loading : %s", CONFIG.disabled_plugins)
        await idle()
        await Mia.stop()
    except Exception as e:
        logging.error(
            f"Could not initialize Telegram client due to a {type(e).__name__}: {e}"
        )
        traceback.print_exc()
        quit()

if __name__ == '__main__':
    if not os.path.exists(CONFIG.work_dir):
        os.makedirs(CONFIG.work_dir)

    event_policy = asyncio.get_event_loop_policy()
    loop = event_policy.get_event_loop()
    loop.run_until_complete(main())
