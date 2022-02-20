import asyncio
import logging
import re
from datetime import timedelta

from telethon import events

from .. import loader

logger = logging.getLogger(__name__)

bak = [
    1785723159,
    1377037394,
    1261343954,
    1015477223,
    880446774,
    635396952,
    547639600,
    553299699,
    412897338,
    449434040,
    388412512,
]


@loader.tds
class KramiikkMod(loader.Module):
    """Алина, я люблю тебя."""

    strings = {"name": "kramiikk"}

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.me = await client.get_me()

    async def err(self, m, p):
        try:
            async with self.client.conversation(m.chat_id) as conv:
                global RSP
                RSP = await conv.wait_event(
                    events.NewMessage(from_users=1124824021,
                                      chats=m.chat_id, pattern=p)
                )
        except asyncio.exceptions.TimeoutError:
            pass

    async def uku(self, m, cmn, txt):
        time = re.search(
            txt,
            RSP.text,
            re.IGNORECASE,
        )
        await self.client.send_message(
            m.chat_id,
            cmn,
            schedule=timedelta(hours=int(time.group(1)),
                               minutes=int(time.group(2))),
        )

    async def buk(self, m):
        p = "🏃‍♂️"
        await self.client.send_message(m.chat_id, "<b>жаба инфо</b>")
        await self.err(m, p)
        cmn = "откормить жабку"
        if "(Откормить через" in RSP.text:
            txt = r"Откормить через (\d+)ч:(\d+)м"
            await self.uku(m, cmn, txt)
        else:
            await self.client.send_message(m.chat_id, cmn)
        if "Можно отправиться" in RSP.text:
            cmn = "отправиться в золотое подземелье"
            await self.client.send_message(m.chat_id, cmn)
        elif (
            "подземелье можно через 2ч"
            and "Жабу можно отправить" in RSP.text
        ):
            cmn = "работа крупье"
            await self.client.send_message(m.chat_id, cmn)
            return await self.client.send_message(
                m.chat_id, "<b>моя жаба</b>"
            )
        elif "В подземелье можно" in RSP.text:
            cmn = "отправиться в золотое подземелье"
            txt = r"подземелье можно через (\d+)ч. (\d+)м."
            await self.uku(m, cmn, txt)

    async def bmj(self, m):
        p = "🏃‍♂️"
        await self.client.send_message(m.chat_id, "<b>жаба инфо</b>")
        await self.err(m, p)
        cmn = "покормить жабку"
        if "покормить через" in RSP.text:
            txt = r"покормить через (\d+)ч:(\d+)м"
            await self.uku(m, cmn, txt)
        else:
            await self.client.send_message(m.chat_id, cmn)
        if "работу можно" in RSP.text:
            cmn = "работа крупье"
            txt = r"будет через (\d+)ч:(\d+)м"
            await self.uku(m, cmn, txt)
        elif "можно отправить" in RSP.text:
            await m.respond("работа крупье")

    async def watcher(self, m):
        if self.me.id in {1486632011}:
            name = "Оботи"
        elif self.me.id in {1286303075}:
            name = "Лавин"
        elif self.me.id in {547639600}:
            name = "Нельс"
        elif self.me.id in {980699009}:
            name = "Лена"
        elif self.me.id in {1423368454}:
            name = "Len"
        elif self.me.id in {230473666}:
            name = "Ваня"
        elif self.me.id in {887255479}:
            name = "Кира"
        elif self.me.id in {1266917477}:
            name = "Артур"
        else:
            name = self.me.first_name
        try:
            if (
                m.message.startswith((name, f"@{self.me.username}"))
            ) and m.sender_id in bak:
                args = m.text
                reply = await m.get_reply_message()
                if "напиши в" in m.message:
                    i = args.split(" ", 4)[3]
                    if i.isnumeric():
                        i = int(i)
                    s = args.split(" ", 4)[4]
                    if reply:
                        s = reply
                    await self.client.send_message(i, s)
                elif "арена" in m.message:
                    p = "•"
                    await self.client.send_message(m.chat_id, "<b>мои жабы</b>")
                    await self.err(m, p)
                    capt = re.findall(r"\| -100(\d+)", RSP.text)
                    for i in capt:
                        await self.client.send_message(int(i), "<b>на арену</b>")
                elif "напади" in m.message:
                    await m.respond("напасть на клан")
                elif "подземелье" in m.message:
                    await m.respond("<b>отправиться в золотое подземелье</b>")
                elif "снаряжение" in m.message:
                    p = "Ваше"
                    await self.client.send_message(m.chat_id, "<b>мое снаряжение</b>")
                    await self.err(m, p)
                    if "Ближний бой: Пусто" in RSP.text:
                        await m.respond("скрафтить клюв цапли")
                    if "Дальний бой: Пусто" in RSP.text:
                        await m.respond("скрафтить букашкомет")
                    if "Наголовник: Пусто" in RSP.text:
                        await m.respond("скрафтить наголовник из клюва цапли")
                    if "Нагрудник: Пусто" in RSP.text:
                        await m.respond("скрафтить нагрудник из клюва цапли")
                    if "Налапники: Пусто" in RSP.text:
                        await m.respond("скрафтить налапники из клюва цапли")
                else:
                    mmsg = args.split(" ", 2)[2]
                    if reply:
                        await reply.reply(mmsg)
                    else:
                        await m.respond(mmsg)
            elif (
                f"Сейчас выбирает ход: {self.me.first_name}" in m.message and m.buttons
            ):
                await m.respond("реанимировать жабу")
                await m.click(0)
            elif (
                m.message.casefold().startswith(("моя жаба", "@toadbot моя жаба"))
                and m.sender_id == self.me.id
            ):
                p = "🐸"
                await self.err(m, p)
                jab = re.search(
                    r"Ур.+: (\d+)[\s\S]*Бу.+: (\d+)", RSP.raw_text)
                if "Живая" not in RSP.text:
                    await m.respond("реанимировать жабу")
                if int(jab.group(1)) > 72 and int(jab.group(3)) > 3750:
                    await self.buk(m)
                else:
                    await self.bmj(m)
                if "жабу можно через" in RSP.text:
                    cmn = "завершить работу"
                    txt = r"через (\d+) часов (\d+) минут"
                    await self.uku(m, cmn, txt)
                elif "жабу с работы" in RSP.text:
                    cmn = "завершить работу"
                    await self.client.send_message(m.chat_id, cmn)
            else:
                return
        finally:
            return
