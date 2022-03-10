import asyncio
import logging
import random
import re
from datetime import timedelta

from telethon import events

from .. import loader, utils

logger = logging.getLogger(__name__)

ded = {
    "Нужна реанимация": "реанимировать жабу",
    "Хорошее": "использовать леденцы 4",
    "жабу с работы": "завершить работу",
    "Можно откормить": "откормить жабку",
    "можно покормить": "покормить жабку",
    "Можно отправиться": "отправиться в золотое подземелье",
    "жаба в данже": "рейд старт",
    "можно отправить": "работа крупье",
    "Можно на арену": "на арену",
    "Используйте атаку": "на арену",
    "золото": "отправиться в золотое подземелье",
    "го кв": "начать клановую войну",
    "напади": "напасть на клан",
    "карту": "отправить карту",
    "туса": "жабу на тусу",
    "Ближний бой: Пусто": "скрафтить клюв цапли",
    "Дальний бой: Пусто": "скрафтить букашкомет",
    "Наголовник: Пусто": "скрафтить наголовник из клюва цапли",
    "Нагрудник: Пусто": "скрафтить нагрудник из клюва цапли",
    "Налапники: Пусто": "скрафтить налапники из клюва цапли",
    "Банда: Пусто": "взять жабу",
}


@loader.tds
class KramiikkMod(loader.Module):
    """Алина, я люблю тебя!"""

    strings = {"name": "Kramiikk"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.su = db.get("Su", "su", {})
        self.sf = db.get("Su", "sf", {})
        self.me = await client.get_me()

    async def sacmd(self, m):
        if "auto" not in self.su:
            self.su.setdefault("auto", {})
            msg = "<b>Автожаба активирована</b>"
        else:
            self.su.pop("auto")
            msg = "<b>Автожаба деактивирована</b>"
        self.db.set("Su", "su", self.su)
        await utils.answer(m, msg)

    async def sfcmd(self, m):
        key = utils.get_args_raw(m)
        key = key.split(" / ")[0]
        val = key.split(" / ")[1]
        if key not in self.sf:
            self.sf.setdefault(key, val)
            msg = "<b>активирована</b>"
        else:
            self.sf.pop(key)
            msg = "<b>деактивирована</b>"
        self.db.set("Su", "sf", self.sf)
        await utils.answer(m, msg)

    async def sncmd(self, m):
        args = utils.get_args_raw(m)
        self.su["name"] = args.casefold()
        await utils.answer(
            m, "👻 <code>" + self.su["name"] + "</code> <b>успешно изменён</b>"
        )
        self.db.set("Su", "su", self.su)

    async def sucmd(self, m):
        args = utils.get_args_raw(m)
        txt = int(args)
        if txt == self.me.id and "name" not in self.su:
            self.su.setdefault("name", self.me.username)
            self.su.setdefault("users", [])
            self.su["users"].append(txt)
            msg = f"👺 <code>{self.me.username}</code> <b>запомните</b>"
        elif txt in self.su["users"]:
            self.su["users"].remove(txt)
            msg = f"🖕🏾 {txt} <b>успешно удален</b>"
        else:
            self.su["users"].append(txt)
            msg = f"🤙🏾 {txt} <b>успешно добавлен</b>"
        self.db.set("Su", "su", self.su)
        await utils.answer(m, msg)

    async def err(self, chat, pattern):
        try:
            async with self.client.conversation(chat) as conv:
                global RSP
                RSP = await conv.wait_event(
                    events.NewMessage(
                        from_users=1124824021, chats=chat, pattern=pattern
                    )
                )
            for i in (i for i in ded if i in RSP.text):
                try:
                    await self.client.send_message(chat, ded[i])
                finally:
                    pass
        except asyncio.exceptions.TimeoutError:
            pass

    async def bmj(self, chat):
        pattern = "🐸"
        await self.err(chat, pattern)
        await self.client.send_message(chat, "жаба инфо")
        pattern = "🏃‍♂️"
        await self.err(chat, pattern)
        if "работы" in RSP.text:
            pattern = "Ваше"
            await self.client.send_message(chat, "мое снаряжение")
            await self.err(chat, pattern)

    async def watcher(self, m):
        args = m.text
        chat = m.chat_id
        me = self.me.id
        name = self.me.username
        users = me
        if "name" in self.su:
            name = self.su["name"]
            users = self.su["users"]
        try:
            if (
                m.message.startswith(("✅", "📉"))
                and m.sender_id in {1124824021}
                and "auto" in self.su
            ):
                await self.client.send_message(
                    1124824021,
                    "мои жабы",
                    schedule=timedelta(
                        minutes=random.randint(13, 60), seconds=random.randint(1, 60)
                    ),
                )
            elif m.message.startswith("мои жабы") and chat in {1124824021}:
                await m.delete()
                pattern = "•"
                await self.err(chat, pattern)
                await RSP.delete()
                await self.client.send_read_acknowledge(chat)
                capt = re.findall(r"\| -100(\d+)", RSP.text)
                for i in capt:
                    try:
                        chat = int(i)
                        await self.client.send_message(chat, "моя жаба")
                        await self.bmj(chat)
                    finally:
                        pass
            elif m.message.casefold().startswith(name) and (m.sender_id in users):
                reply = await m.get_reply_message()
                if "напиши в " in m.message:
                    chat = args.split(" ", 4)[3]
                    if chat.isnumeric():
                        chat = int(chat)
                    if reply:
                        msg = reply
                    else:
                        msg = args.split(" ", 4)[4]
                    await self.client.send_message(chat, msg)
                elif "напиши" in m.message:
                    msg = args.split(" ", 2)[2]
                    if reply:
                        await reply.reply(msg)
                    else:
                        await m.respond(msg)
                else:
                    cmn = args.split(" ", 1)[1]
                    if cmn in ded:
                        await m.reply(ded[cmn])
            elif (
                f"Сейчас выбирает ход: {self.me.first_name}" in m.message and m.buttons
            ):
                await m.respond("реанимировать жабу")
                await m.click(0)
            elif (
                not m.message.endswith(("[1👴🐝]", "[1🦠🐝]", "👑🐝"))
                and m.buttons
                and m.sender_id in {830605725}
            ):
                await m.click(0)
            elif "НЕЗАЧЁТ!" in m.message:
                args = [int(x) for x in m.text.split() if x.isnumeric()]
                delta = timedelta(hours=args[1], minutes=args[2], seconds=33)
                await self.client.send_message(
                    707693258, "<b>Фарма</b>", schedule=delta
                )
            else:
                for i in (i for i in self.sf if i in m.message):
                    try:
                        await self.client.send_message(chat, self.sf[i])
                    finally:
                        pass
        finally:
            return
