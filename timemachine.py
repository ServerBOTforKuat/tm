import time
import asyncio
import logging
import datetime
import threading
from asyncio import sleep
from .. import loader, utils
from apscheduler.triggers.cron import CronTrigger
from telethon.tl.functions.users import GetFullUserRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest

# requires: apscheduler

logger = logging.getLogger(__name__)

@loader.tds
class SchedMod(loader.Module):
    """sched"""
    strings = {'name': 'Sched'}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

        map = 707693258

        async def zaraz():
            for number in range (7):
                await client.send_message(map, 'заразить р')
                await sleep (13)

        async def off():
            firstname = "ʍօղɑɾϲհ 🔴(афк)"
            lastname = " "
            await client(UpdateProfileRequest(first_name=firstname, last_name=lastname))

        scheduler = AsyncIOScheduler()
<<<<<<< Updated upstream
        scheduler.add_job(zaraz, CronTrigger.from_crontab('*/25 * * * *', timezone='Europe/Moscow'))
=======
        scheduler.add_job(zaraz, CronTrigger.from_crontab('*/30 * * * *', timezone='Europe/Moscow'))
        scheduler.add_job(off, CronTrigger.from_crontab('*/3 * * * *', timezone='Europe/Moscow'))
>>>>>>> Stashed changes
        scheduler.start()

        asyncio.get_event_loop().run_forever()
