import asyncio
import logging
import random
import re
from datetime import timedelta

from aiogram.types import *
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

    async def bmj(self, chat):
        """алгоритм жабабота"""
        pattern = "🐸"
        await self.err(chat, pattern)
        for i in (i for i in ded if i in RSP.text):
            await self.client.send_message(chat, ded[i])
        jab = re.search(r"У.+: (\d+)[\s\S]*Б.+: (\d+)", RSP.text)
        await self.client.send_message(chat, "жаба инфо")
        pattern = "🏃‍♂️"
        await self.err(chat, pattern)
        for i in (i for i in ded if i in RSP.text):
            if (
                int(jab.group(1)) < 111
                or (int(jab.group(1)) > 111 and int(jab.group(2)) < 2222)
            ) and (i == "Можно откормить" or i == "Можно отправиться"):
                continue
            await self.client.send_message(chat, ded[i])
        if "работы" in RSP.text:
            pattern = "Ваше"
            await self.client.send_message(chat, "мое снаряжение")
            await self.err(chat, pattern)
            for i in (i for i in ded if i in RSP.text):
                await self.client.send_message(chat, ded[i])

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.su = db.get("Su", "su", {})
        self.me = await client.get_me()

    async def err(self, chat, pattern):
        """работа с ответом жабабота"""
        try:
            async with self.client.conversation(chat) as conv:
                global RSP
                RSP = await conv.wait_event(
                    events.NewMessage(
                        from_users=1124824021, chats=chat, pattern=pattern
                    )
                )
        except asyncio.exceptions.TimeoutError:
            pass

    async def hrs(self, m, msg):
        await self.inline.form(
            msg,
            message=m,
            reply_markup=[
                [
                    {
                        "text": "📜",
                        "callback": self.inline__handler,
                        "args": (True,),
                    },
                    {
                        "text": "🗿",
                        "callback": self.inline__handler,
                        "args": (False,),
                    },
                ]
            ],
            force_me=False,
        )

    async def inline__handler(self, call: CallbackQuery, correct: bool) -> None:
        if not correct:
            s = await self.client.get_messages(1767017980, limit=42)
            msg = "<b>Сейчас в кв:\n</b>"
            t = await self.client.send_message(1782816965, "Сезон кланов золото")
            for i in s:
                await self.tms(t, i)
                if "VS" in i.text and timedelta(days=0) <= MS < timedelta(
                    hours=4, minutes=3
                ):
                    msg += f"\n{i.message}\n<i>Время кв: {MS}</i>\n"
        else:
            src = f"Клан Вадим и его жабехи Состав:"
            msg = f"Клан Вадим и его жабехи:\n"
            get = await self.client.get_messages(1655814348, search=src)
            for i in get:
                ids = re.search(r"id: (.+)", i.text).group(1)
                reg = re.findall(r"\n(\d+)", i.text)
                for s in reg:
                    src = f"{ids} {s} Уровень:"
                    get = await self.client.get_messages(1655814348, search=src)
                    for p in get:
                        ger = re.search(r"ь: (\d+)", p.text)
                        msg += f"\nУровень: {ger.group(1)}"
                        if "Жаба:" in p.text:
                            ger = re.search(r"а: (.+)", p.text).group(1)
                            msg += f" Жаба: {ger}"
            msg += f"\n\n{call.from_user.id}"
        await call.edit(msg)
        await asyncio.sleep(10)
        await call.edit(
            "нажми",
            reply_markup=[
                [
                    {
                        "text": "📜",
                        "callback": self.ler,
                        "args": (True,),
                    },
                    {
                        "text": "😈",
                        "url": "t.me/k_uat",
                    },
                    {
                        "text": "🗿",
                        "callback": self.ler,
                        "args": (False,),
                    },
                ]
            ],
        )

    async def ler(self, call: CallbackQuery, correct: bool) -> None:
        if not correct:
            s = await self.client.get_messages(1788178824, limit=42)
            msg = "Чат:\n"
            for i in s:
                msg += f"\n{i.message}"
        else:
            msg = f"{call.from_user.id}"
        await call.edit(msg)

    async def sacmd(self, m):
        """будет смотреть за вашими жабами"""
        if "auto" not in self.su:
            self.su.setdefault("auto", {})
            msg = "<b>активирована</b>"
        else:
            self.su.pop("auto")
            msg = "<b>деактивирована</b>"
        self.db.set("Su", "su", self.su)
        await self.hrs(m, msg)

    async def sfcmd(self, m):
        """добавить фильтры, пример 'текст / ответ'"""
        chatid = str(m.chat_id)
        msg = utils.get_args_raw(m)
        key = msg.split(" / ")[0]
        if not msg:
            txt = ""
            for i in self.su[chatid]:
                txt += f"<b>• {i}</b>\n"
            return await utils.answer(
                m, f"<b>Фильтры: {len(self.su[chatid])}\n\n{txt}</b>"
            )
        if chatid not in self.su:
            self.su.setdefault(chatid, {})
        if key not in self.su[chatid]:
            self.su[chatid].setdefault(key, msg.split(" / ")[1])
            msg = "<b>добавлен</b>"
        else:
            self.su[chatid].pop(key)
            msg = "<b>удален</b>"
        if self.su[chatid] == {}:
            self.su.pop(chatid)
        self.db.set("Su", "su", self.su)
        await self.hrs(m, msg)

    async def stcmd(self, m):
        """фильтр на юзера, пример 'ид / текст / ответ'"""
        chatid = str(m.chat_id)
        msg = utils.get_args_raw(m)
        idu = msg.split(" / ")[0]
        key = msg.split(" / ")[1]
        if chatid not in self.su:
            self.su.setdefault(chatid, {})
        if idu not in self.su[chatid]:
            self.su[chatid].setdefault(idu, {})
        if key not in self.su[chatid][idu]:
            self.su[chatid][idu].setdefault(key, msg.split(" / ")[2])
            msg = "<b>активирована</b>"
        else:
            self.su[chatid][idu].pop(msg.split(" / ")[0])
            msg = "<b>деактивирована</b>"
        self.db.set("Su", "su", self.su)
        await self.hrs(m, msg)

    async def sncmd(self, m):
        """ник для команд"""
        msg = utils.get_args_raw(m)
        self.su["name"] = msg.casefold()
        msg = "👻 <code>" + self.su["name"] + "</code> <b>успешно изменён</b>"
        await self.hrs(m, msg)
        self.db.set("Su", "su", self.su)

    async def sucmd(self, m):
        """добавляет пользователей для управление акк"""
        msg = utils.get_args_raw(m)
        txt = int(msg)
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
        await self.hrs(m, msg)

    async def tms(self, t, i):
        global MS
        MS = timedelta(
            hours=t.date.hour, minutes=t.date.minute, seconds=t.date.second
        ) - timedelta(hours=i.date.hour, minutes=i.date.minute, seconds=i.date.second)

    async def watcher(self, m):
        msg = m.text
        chat = m.chat_id
        chatid = str(chat)
        idu = m.sender_id
        me = self.me.id
        name = self.me.username
        users = me
        if "name" in self.su:
            name = self.su["name"]
            users = self.su["users"]
        try:
            if (
                m.message.startswith(("✅", "📉"))
                and idu in {1124824021}
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
            elif m.message.casefold().startswith(name) and (idu in users):
                reply = await m.get_reply_message()
                if "напиши в " in m.message:
                    chat = msg.split(" ", 4)[3]
                    if chat.isnumeric():
                        chat = int(chat)
                    if reply:
                        msg = reply
                    else:
                        msg = msg.split(" ", 4)[4]
                    await self.client.send_message(chat, msg)
                elif "напиши" in m.message:
                    async with self.client.conversation(chat):
                        msg = msg.split(" ", 2)[2]
                        if reply:
                            await reply.reply(msg)
                        else:
                            await self.hrs(m, msg)
                else:
                    cmn = msg.split(" ", 1)[1]
                    if cmn in ded:
                        await m.reply(ded[cmn])
            elif (
                f"Сейчас выбирает ход: {self.me.first_name}" in m.message and m.buttons
            ):
                msg = "реанимировать жабу"
                await self.hrs(m, msg)
                await m.click(0)
            elif (
                not m.message.endswith(("[1👴🐝]", "[1🦠🐝]", "👑🐝"))
                and m.buttons
                and idu in {830605725}
            ):
                await m.click(0)
            elif "НЕЗАЧЁТ!" in m.message:
                msg = [int(x) for x in m.text.split() if x.isnumeric()]
                delta = timedelta(hours=msg[1], minutes=msg[2], seconds=33)
                await self.client.send_message(
                    707693258, "<b>Фарма</b>", schedule=delta
                )
            elif chatid in self.su:
                idu = str(idu)
                if idu in self.su[chatid]:
                    for i in (i for i in self.su[chatid][idu] if i in m.message):
                        await utils.answer(m, self.su[chatid][idu][i])
                for i in (i for i in self.su[chatid] if i in m.message):
                    await utils.answer(m, self.su[chatid][i])
            else:
                return
        finally:
            return
