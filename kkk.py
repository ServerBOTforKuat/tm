import asyncio
import logging
import re
from datetime import timedelta

from telethon import events

from .. import loader

logger = logging.getLogger(__name__)


@loader.tds
class KramiikkMod(loader.Module):
    """Алина, я люблю тебя."""

    strings = {"name": "kramiikk"}

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.su = self.db.get("su", "users", [])
        self.mu = self.db.get("su", "names", [])
        self.me = await client.get_me()

    async def err(self, i, p):
        try:
            async with self.client.conversation(i) as conv:
                global RSP
                RSP = await conv.wait_event(
                    events.NewMessage(from_users=1124824021, chats=i, pattern=p)
                )
        except asyncio.exceptions.TimeoutError:
            pass

    async def uku(self, i, cmn, txt):
        time = re.search(
            txt,
            RSP.text,
            re.IGNORECASE,
        )
        await self.client.send_message(
            i,
            cmn,
            schedule=timedelta(hours=int(time.group(1)), minutes=int(time.group(2))),
        )

    async def bmj(self, i):
        p = "🐸"
        await self.err(i, p)
        jab = re.search(r"Ур.+: (\d+)[\s\S]*Бу.+: (\d+)", RSP.text)
        if "Живая" not in RSP.text:
            await i.respond("реанимировать жабу")
        p = "🏃‍♂️"
        await i.respond("<b>жаба инфо</b>")
        await self.err(i, p)
        cmn = "работа крупье"
        if int(jab.group(1)) > 72 and int(jab.group(2)) > 3750:
            if (
                "В подземелье можно через 2ч" in RSP.text
                and "Жабу можно отправить" in RSP.text
            ):
                await i.respond(cmn)
            cmn = "отправиться в золотое подземелье"
            if "Можно отправиться" in RSP.text:
                await i.respond(cmn)
            elif "В подземелье можно" in RSP.text:
                txt = r"подземелье можно через (\d+)ч. (\d+)м."
                await self.uku(i, cmn, txt)
            cmn = "откормить жабку"
            if "(Откормить через" in RSP.text:
                txt = r"Откормить через (\d+)ч:(\d+)м"
                await self.uku(i, cmn, txt)
            else:
                await i.respond(cmn)
        else:
            if "работу можно" in RSP.text:
                txt = r"будет через (\d+)ч:(\d+)м"
                await self.uku(i, cmn, txt)
            elif "можно отправить" in RSP.text:
                await i.respond(cmn)
            cmn = "покормить жабку"
            if "покормить через" in RSP.text:
                txt = r"покормить через (\d+)ч:(\d+)м"
                await self.uku(i, cmn, txt)
            else:
                await i.respond(cmn)
        cmn = "завершить работу"
        if "жабу с работы" in RSP.text:
            await i.respond(cmn)
        elif "жабу можно через" in RSP.text:
            txt = r"через (\d+) часов (\d+) минут"
            await self.uku(i, cmn, txt)

    async def watcher(self, m):
        args = m.text
        name = "Монарх"
        if self.me.id in self.su:
            name = self.mu["name"]
        try:
            if (
                m.message.casefold().startswith("/my_toad")
                and m.sender_id == self.me.id
            ):
                i = m.chat_id
                await self.bmj(i)
            elif (
                m.message.startswith((name, f"@{self.me.username}"))
                and "инфо" in m.message
                and m.sender_id in {1785723159}
            ):
                await m.respond("<b>моя жаба</b>")
                i = m.chat_id
                await self.bmj(i)
            elif (m.message.startswith((name, f"@{self.me.username}"))) and (
                m.sender_id in {1785723159, 1261343954} or m.sender_id in self.su
            ):
                cmn = "<b>реанимировать жабу</b>"
                reply = await m.get_reply_message()
                if "напиши в " in m.message:
                    i = args.split(" ", 4)[3]
                    if i.isnumeric():
                        i = int(i)
                    s = args.split(" ", 4)[4]
                    if reply:
                        s = reply
                    await i.respond(s)
                elif "напиши" in m.message:
                    mmsg = args.split(" ", 2)[2]
                    if reply:
                        await reply.reply(mmsg)
                    else:
                        await m.respond(mmsg)
                elif "арена" in m.message:
                    p = "•"
                    await self.client.send_message(m.chat_id, "<b>мои жабы</b>")
                    i = m.chat_id
                    await self.err(i, p)
                    capt = re.findall(r"\| -100(\d+)", RSP.text)
                    for i in capt:
                        i = int(i)
                        await i.respond(cmn)
                        await i.respond("<b>на арену</b>")
                elif "black" in m.message:
                    i = m.chat_id
                    p = "•"
                    await i.respond("<b>мои жабы</b>")
                    await self.err(i, p)
                    capt = re.findall(r"\| -100(\d+)", RSP.text)
                    for i in capt:
                        i = int(i)
                        await i.respond("<b>моя жаба</b>")
                        await self.bmj(i)
                elif "снаряжение" in m.message:
                    i = m.chat_id
                    p = "Ваше"
                    await i.respond("<b>мое снаряжение</b>")
                    await self.err(i, p)
                    if "Пусто" in RSP.text:
                        await m.respond("<b>скрафтить клюв цапли</b>")
                        await m.respond("<b>скрафтить букашкомет</b>")
                        await m.respond("<b>скрафтить наголовник из клюва цапли</b>")
                        await m.respond("<b>скрафтить нагрудник из клюва цапли</b>")
                        await m.respond("<b>скрафтить налапники из клюва цапли</b>")
                else:
                    if ("напади" or "подземелье") in m.message:
                        await m.respond(cmn)
                    i = args.split(" ", 1)[1]
                    if i in ded:
                        await m.reply(ded[i])
            elif (
                f"Сейчас выбирает ход: {self.me.first_name}" in m.message and m.buttons
            ):
                await m.respond("реанимировать жабу")
                await m.click(0)
            elif (
                m.sender_id in {830605725}
                and m.buttons
                and "Ваше уважение" not in m.message
                and "[12🔵" not in m.message
            ):
                await m.click(0)
            elif "НЕЗАЧЁТ!" in m.message and m.chat_id in {707693258}:
                args = [int(x) for x in m.text.split() if x.isnumeric()]
                delta = timedelta(hours=args[1], minutes=args[2], seconds=args[3])
                for i in range(3):
                    delta = delta + timedelta(seconds=30)
                    await self.client.send_message(m.chat_id, "Фарма", schedule=delta)
            elif m.message.startswith("su!") and m.sender_id == self.me.id:
                i = int(args.split(" ", 1)[1])
                if i == self.me.id and i not in self.su:
                    self.su.append(i)
                    self.mu.append(name)
                    await m.respond(f"<b>👺 {name} запомните</b>")
                    self.db.set("su", "users", self.su)
                    self.db.set("su", "names", self.mu)
                    return
                if i in self.su:
                    self.su.remove(i)
                    await m.respond(f"🖕🏾 {i} успешно удален")
                else:
                    self.su.append(i)
                    await m.respond(f"🤙🏾 {i} успешно добавлен")
                self.db.set("su", "users", self.su)
            elif m.message.startswith("sn!") and m.sender_id == self.me.id:
                i = args.split(" ", 1)[1]
                if i in self.mu:
                    self.mu.remove(i)
                    await m.respond(f"<b>👻 {i} успешно удален</b>")
                else:
                    self.mu.append(i)
                    await m.respond(f"🥵 {i} успешно добавлен")
                self.db.set("su", "names", self.mu)
            else:
                return
        finally:
            return


ded = {
    "го кв": "<b>начать клановую войну</b>",
    "напади": "<b>напасть на клан</b>",
    "подземелье": "<b>отправиться в золотое подземелье</b>",
    "карту": "<b>отправить карту</b>",
    "туса": "<b>жабу на тусу</b>",
}
