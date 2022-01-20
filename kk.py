import asyncio
import datetime
import logging
import random
import re

from telethon import events, functions

from .. import loader, utils

logger = logging.getLogger(__name__)
bak = [
    1261343954,
    547639600,
    553299699,
    412897338,
    449434040,
    388412512,
]
elj = [
    -1001441941681,
    -1001436786642,
    -1001380664241,
    -1001289617428,
    -1001485617300,
    -1001465870466,
    -1001169549362,
    -1001543064221,
]
klw = [-419726290, -1001543064221, -577735616, -1001493923839]
ninja = [
    -1001380664241,
    -1001441941681,
    -1001289617428,
    -1001436786642,
    -1001447960786,
    -1001290958283,
    -1001485617300,
]
nr = [1, 3, 5, 7, 9]


def register(cb):
    """.

    ----------

    """
    cb(kramiikkMod())


@loader.tds
class kramiikkMod(loader.Module):
    """Алина, я люблю тебя."""

    answers = {
        0: ("Ответ тебе известен", "Ты знаешь лучше меня!", "Ответ убил!.."),
        1: ("Да, но есть помехи", "Может быть", "Вероятно", "Возможно", "Наверняка"),
        2: ("Есть помехи...", "Вряд ли", "Что-то помешает", "Маловероятно"),
        3: ("Нет, но пока", "Скоро!", "Жди!", "Пока нет"),
    }
    strings = {
        "name": "kramiikk",
        "quest_answer": "<i>%answer%</i>",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        """.

        ----------

        """
        self.client = client
        self.db = db
        self.me = await client.get_me()

    async def watcher(self, message):
        """.

        ----------

        """
        chat = message.chat_id
        name = "монарх"
        rh = random.choice(nr)
        rd = random.randint(rh, 13)
        try:
            if (
                message.message.lower().startswith(
                    ("начать клановую", "@tgtoadbot начать клановую")
                )
                and chat in ninja
            ):
                async with self.client.conversation(chat) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=chat,
                        )
                    )
                    response = await response
                    await conv.cancel_all()
                if "Отлично! Как только" in response.text:
                    src = f"Chat id: {chat} {message.sender_id} Клан:"
                    ms = await self.client.get_messages(1655814348, search=src)
                    if ms.total == 0:
                        return await self.client.send_message(
                            1767017980,
                            f"<i>В поиске {message.sender.first_name}</i>",
                        )
                    for i in ms:
                        klan = re.search("Клан: (.+)", i.message).group(1)
                        if "Усилитель:" in i.message:
                            liga = re.search("Лига: (.+)", i.message).group(1)
                            usil = re.search("Усилитель: (.+)", i.message).group(1)
                            lif = f"\nЛига: {liga}\nУсилитель: {usil}"
                        else:
                            src = f"Топ 35 кланов {klan}"
                            ms = await self.client.get_messages(1782816965, search=src)
                            for i in ms:
                                liga = re.search(
                                    "Топ 35 кланов (.+) лиге", i.message
                                ).group(1)
                                lif = f"\nЛига: {liga}"
                        txt = f"В поиске {klan}{lif}"
                    await self.client.send_message(1767017980, txt)
            elif (
                message.message.lower().startswith((name, f"@{self.me.username}"))
                or (name in message.message and message.message.endswith("😉"))
                and message.sender_id in bak
            ):
                await asyncio.sleep(rd)
                args = message.message
                reply = await message.get_reply_message()
                count = args.split(" ", 2)[1]
                if "захват топа" in message.message:
                    args = message.message
                    reply = await message.get_reply_message()
                    szn = args.split(" ", 2)[2]
                    await self.client.send_message(chat, f"сезон кланов {szn}")
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=chat,
                            )
                        )
                        response = await response
                        await conv.cancel_all()
                    result = re.findall("(\d+)\. 🛡(\d+) \| (.*)", response.text)
                    rep = "🧛🏿Захваченные в этом сезоне🧛🏿\n(Победы | Название | Наказание):"
                    for item in result:
                        src = f"{item[2]} Усилитель:"
                        ms = await self.client.get_messages(1655814348, search=src)
                        if ms.total != 0:
                            a = "<i>😈Захвачен</i>"
                        else:
                            a = "<i>🌚Кто это...</i>"
                        rep += f"\n{item[0]}.🛡{item[1]} | {item[2]} | {a}"
                    await response.reply(rep)
                elif "напади" in message.message:
                    await self.client.send_message(chat, "напасть на клан")
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=chat,
                            )
                        )
                        response = await response
                        await conv.cancel_all()
                    if "Ваша жаба на" in response.text:
                        await self.client.send_message(chat, "завершить работу")
                        await self.client.send_message(chat, "реанимировать жабу")
                        await self.client.send_message(chat, "напасть на клан")
                    elif "Ваша жаба сейчас" in response.text:
                        await self.client.send_message(chat, "выйти из подземелья")
                        await self.client.send_message(chat, "реанимировать жабу")
                        await self.client.send_message(chat, "напасть на клан")
                elif "напиши в" in message.message:
                    chan = args.split(" ", 4)[3]
                    if chan.isnumeric():
                        chan = int(args.split(" ", 4)[3])
                    mmsg = args.split(" ", 4)[4]
                    await self.client.send_message(chan, mmsg)
                elif "подземелье" in message.message:
                    await self.client.send_message(
                        chat, "отправиться в золотое подземелье"
                    )
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=chat,
                            )
                        )
                        response = await response
                        await conv.cancel_all()
                    if "Пожалейте жабу," in response.text:
                        await self.client.send_message(chat, "завершить работу")
                        await self.client.send_message(chat, "реанимировать жабу")
                        await self.client.send_message(
                            chat,
                            "<b>отправиться в золотое подземелье</b>",
                        )
                    elif "Ваша жаба при" in response.text:
                        await self.client.send_message(chat, "реанимировать жабу")
                        await self.client.send_message(
                            chat,
                            "<b>отправиться в золотое подземелье</b>",
                        )
                elif "снаряжение" in message.message:
                    await self.client.send_message(chat, "мое снаряжение")
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=chat,
                            )
                        )
                        response = await response
                        await conv.cancel_all()
                    if "Ближний бой: Пусто" in response.text:
                        await self.client.send_message(chat, "скрафтить клюв цапли")
                    if "Дальний бой: Пусто" in response.text:
                        await self.client.send_message(chat, "скрафтить букашкомет")
                    if "Наголовник: Пусто" in response.text:
                        await self.client.send_message(
                            chat,
                            "скрафтить наголовник из клюва цапли",
                        )
                    if "Нагрудник: Пусто" in response.text:
                        await self.client.send_message(
                            chat,
                            "скрафтить нагрудник из клюва цапли",
                        )
                    if "Налапники: Пусто" in response.text:
                        await self.client.send_message(
                            chat,
                            "скрафтить налапники из клюва цапли",
                        )
                    if "Банда: Пусто" in response.text:
                        await self.client.send_message(chat, "взять жабу")
                        response = await response
                        if "У тебя уже есть" in response.text:
                            await self.client.send_message(chat, "собрать банду")
                        else:
                            await self.client.send_message(
                                chat,
                                "взять жабу",
                                schedule=datetime.timedelta(hours=2),
                            )
                elif message.message.endswith("?"):
                    words = re.findall(r"\w+", f"{message.message}")
                    words_len = [words.__len__()] + [x.__len__() for x in words]
                    i = words_len.__len__()
                    while i > 1:
                        i -= 1
                        for x in range(i):
                            words_len[x] = (
                                words_len[x] + words_len[x + 1] - 3
                                if words_len[x] + words_len[x + 1] > 3
                                else words_len[x] + words_len[x + 1]
                            )
                    await message.reply(
                        self.strings["quest_answer"].replace(
                            "%answer%", random.choice(self.answers[words_len[0]])
                        )
                    )
                elif "реплай" in message.message:
                    sct = args.split(" ", 4)[2]
                    if sct.isnumeric():
                        sct = int(args.split(" ", 4)[2])
                    sak = args.split(" ", 4)[3]
                    if sak.isnumeric():
                        sak = int(args.split(" ", 4)[3])
                    ms = await self.client.get_messages(sct, ids=sak)
                    mmsg = args.split(" ", 4)[4]
                    await ms.reply(mmsg)
                elif message.message.lower().startswith("лвл чек"):
                    x = int(message.message.split(" ", 3)[2])
                    u = int(message.message.split(" ", 3)[3])
                    y = ((x + u) - 160) * 2
                    if y > -1:
                        res = f"<b>~ {y} лвл</b>"
                        await utils.answer(message, res)
                elif "туса" in message.message:
                    await message.respond("жабу на тусу")
                elif "го кв" in message.message:
                    await message.respond("начать клановую войну")
                elif count.isnumeric() and reply:
                    count = int(args.split(" ", 3)[1])
                    mmsg = args.split(" ", 3)[3]
                    time = int(args.split(" ", 3)[2])
                    for _ in range(count):
                        await reply.reply(mmsg)
                        await asyncio.sleep(time)
                elif count.isnumeric():
                    count = int(args.split(" ", 3)[1])
                    mmsg = args.split(" ", 3)[3]
                    time = int(args.split(" ", 3)[2])
                    for _ in range(count):
                        await self.client.send_message(chat, mmsg)
                        await asyncio.sleep(time)
                else:
                    mmsg = args.split(" ", 2)[2]
                    if reply:
                        await reply.reply(mmsg)
                    else:
                        await utils.answer(message, mmsg)
            elif (
                message.message.lower().startswith("букашки мне😊")
                and message.sender_id in bak
            ):
                await asyncio.sleep(rd)
                await self.client.send_message(chat, "мой баланс")
                async with self.client.conversation(chat) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=chat,
                        )
                    )
                    response = await response
                    await conv.cancel_all()
                bug = int(
                    re.search("жабы: (\d+)", response.text, re.IGNORECASE).group(1)
                )
                if bug < 100:
                    await utils.answer(message, "осталось для похода")
                else:
                    while bug > 50049:
                        await utils.answer(message, "отправить букашки 50000")
                        bug -= 50000
                    snt = bug - 50
                    await utils.answer(message, f"отправить букашки {snt}")
            elif (
                message.message.lower().startswith("инвентарь мне😊")
                and message.sender_id in bak
            ):
                await asyncio.sleep(rd)
                await self.client.send_message(chat, "мой инвентарь")
                async with self.client.conversation(chat) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=chat,
                        )
                    )
                    response = await response
                    await conv.cancel_all()
                cnd = int(
                    re.search("Леденцы: (\d+)", response.text, re.IGNORECASE).group(1)
                )
                apt = int(
                    re.search("Аптечки: (\d+)", response.text, re.IGNORECASE).group(1)
                )
                if cnd > 0:
                    if cnd > 49:
                        await utils.answer(message, "отправить леденцы 50")
                    else:
                        await utils.answer(message, f"отправить леденцы {cnd}")
                    if apt > 9:
                        await utils.answer(message, "отправить аптечки 10")
                    else:
                        await utils.answer(message, f"отправить аптечки {apt}")
            elif (
                message.message.lower().startswith(("доброе утро", "спокойной ночи"))
                and message.sender_id in bak
            ):
                sch = (
                    await self.client(
                        functions.messages.GetScheduledHistoryRequest(chat, 0)
                    )
                ).messages
                await self.client(
                    functions.messages.DeleteScheduledMessagesRequest(
                        chat, id=[x.id for x in sch]
                    )
                )
                if chat in elj:
                    await self.client.send_message(chat, "Жаба инфо")
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=chat,
                            )
                        )
                        response = await response
                        await conv.cancel_all()
                    if "(Откормить через" in response.text:
                        time_f = re.search(
                            "Откормить через (\d+)ч:(\d+)м",
                            response.text,
                            re.IGNORECASE,
                        )
                        if time_f:
                            hrs = int(time_f.group(1))
                            min = int(time_f.group(2))
                            delta = datetime.timedelta(
                                hours=hrs, minutes=min, seconds=3
                            )
                            await self.client.send_message(
                                chat, "откормить жабку", schedule=delta
                            )
                    else:
                        await self.client.send_message(chat, "откормить жабку")
                        delta = datetime.timedelta(hours=4, seconds=3)
                        await self.client.send_message(
                            chat, "откормить жабку", schedule=delta
                        )
                    for i in range(4):
                        delta = delta + datetime.timedelta(hours=4)
                        await self.client.send_message(
                            chat, "откормить жабку", schedule=delta
                        )
                    if "В подземелье можно" in response.text:
                        dng_s = re.search(
                            "подземелье можно через (\d+)ч. (\d+)м.",
                            response.text,
                            re.IGNORECASE,
                        )
                        hrs = int(dng_s.group(1))
                        min = int(dng_s.group(2))
                        delta = datetime.timedelta(
                            hours=hrs, minutes=min, seconds=3
                        )
                        await self.client.send_message(
                            chat, "реанимировать жабу", schedule=delta
                        )
                        await self.client.send_message(
                            chat,
                            "Отправиться в золотое подземелье",
                            schedule=delta + datetime.timedelta(seconds=13),
                        )
                        
                        await self.client.send_message(chat, "война инфо")
                        response = await response
                        if "Состояние" in response.text:
                            if chat in klw:
                                await self.client.send_message(
                                    chat, "начать клановую войну"
                                )
                        elif f"{self.me.first_name} | Не атаковал" in response.text:
                            await self.client.send_message(
                            chat, "Напасть на клан"
                            )
                        if hrs>1:
                            await self.client.send_message(chat, "реанимировать жабу")
                            await self.client.send_message(chat, "работа крупье")
                            delta = datetime.timedelta(hours=2, seconds=3)
                            await self.client.send_message(
                                chat, "завершить работу", schedule=delta
                            )
                        for i in range(2):
                            delta = delta + datetime.timedelta(hours=6, seconds=3)
                            await self.client.send_message(
                                chat, "реанимировать жабу", schedule=delta
                            )
                            await self.client.send_message(
                                chat,
                                "работа крупье",
                                schedule=delta + datetime.timedelta(seconds=3),
                            )
                            await self.client.send_message(
                                chat,
                                "завершить работу",
                                schedule=delta + datetime.timedelta(hours=2, seconds=13),
                            )
                    elif "Забрать жабу можно" in response.text:
                        dng_s = re.search(
                            "жабу можно через (\d+) часов (\d+) минут",
                            response.text,
                            re.IGNORECASE,
                        )
                        if dng_s:
                            hrs = int(dng_s.group(1))
                            min = int(dng_s.group(2))
                            delta = datetime.timedelta(
                                hours=hrs, minutes=min, seconds=3
                            )
                            await self.client.send_message(
                                chat, "завершить работу", schedule=delta
                            )
                            await self.client.send_message(
                                chat,
                                "реанимировать жабку",
                                schedule=delta
                                + datetime.timedelta(minutes=25, seconds=3),
                            )
                            await self.client.send_message(
                                chat,
                                "Отправиться в золотое подземелье",
                                schedule=delta
                                + datetime.timedelta(minutes=45, seconds=13),
                            )
                else:
                    await self.client.send_message(chat, "жаба инфо")
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=chat,
                            )
                        )
                        response = await response
                    await conv.cancel_all()
                    if "покормить через" in response.text:
                        time_n = re.search(
                            "покормить через (\d+)ч:(\d+)м",
                            response.text,
                            re.IGNORECASE,
                        )
                        if time_n:
                            hrs = int(time_n.group(1))
                            min = int(time_n.group(2))
                            delta = datetime.timedelta(
                                hours=hrs, minutes=min, seconds=3
                            )
                            await self.client.send_message(
                                chat, "покормить жабку", schedule=delta
                            )
                    else:
                        delta = datetime.timedelta(hours=6, seconds=3)
                        await self.client.send_message(chat, "покормить жабку")
                    for i in range(3):
                        delta = delta + datetime.timedelta(hours=6, seconds=3)
                        await self.client.send_message(
                            chat, "покормить жабку", schedule=delta
                        )
                    if "работу можно" in response.text:
                        time_j = re.search(
                            "будет через (\d+)ч:(\d+)м",
                            response.text,
                            re.IGNORECASE,
                        )
                        if time_j:
                            hrs = int(time_j.group(1))
                            min = int(time_j.group(2))
                            delta = datetime.timedelta(
                                hours=hrs, minutes=min, seconds=3
                            )
                            await self.client.send_message(
                                chat, "реанимировать жабу", schedule=delta
                            )
                            await self.client.send_message(
                                chat,
                                "работа крупье",
                                schedule=delta + datetime.timedelta(seconds=13),
                            )
                        for i in range(2):
                            delta = delta + datetime.timedelta(hours=8)
                            await self.client.send_message(
                                chat, "реанимировать жабу", schedule=delta
                            )
                            await self.client.send_message(
                                chat,
                                "работа крупье",
                                schedule=delta + datetime.timedelta(seconds=13),
                            )
                            await self.client.send_message(
                                chat,
                                "завершить работу",
                                schedule=delta
                                + datetime.timedelta(hours=2, seconds=13),
                            )
                    if "жабу можно через" in response.text:
                        time_r = re.search(
                            "через (\d+) часов (\d+) минут",
                            response.text,
                            re.IGNORECASE,
                        )
                        if time_r:
                            hrs = int(time_r.group(1))
                            min = int(time_r.group(2))
                            delta = datetime.timedelta(
                                hours=hrs, minutes=min, seconds=3
                            )
                            await self.client.send_message(
                                chat, "завершить работу", schedule=delta
                            )
                    elif "можно отправить" in response.text:
                        await self.client.send_message(chat, "реанимировать жабу")
                        await self.client.send_message(chat, "работа крупье")
                        delta = datetime.timedelta(hours=2, seconds=3)
                        await self.client.send_message(
                            chat, "завершить работу", schedule=delta
                        )
                    else:
                        await self.client.send_message(chat, "завершить работу")
                        delta = datetime.timedelta(hours=6)
                    for i in range(2):
                        delta = delta + datetime.timedelta(hours=6, seconds=3)
                        await self.client.send_message(
                            chat, "реанимировать жабу", schedule=delta
                        )
                        await self.client.send_message(
                            chat,
                            "работа крупье",
                            schedule=delta + datetime.timedelta(seconds=3),
                        )
                        await self.client.send_message(
                            chat,
                            "завершить работу",
                            schedule=delta + datetime.timedelta(hours=2, seconds=13),
                        )
            elif (
                f"Сейчас выбирает ход: {self.me.first_name}" in message.message
                and message.buttons
            ):
                await message.respond("реанимировать жабу")
                await message.click(0)
            elif "[8🐝]" in message.message and message.buttons:
                await message.click(0)
            elif "[4🐝]" in message.message and message.buttons:
                await message.click(0)
            elif "[2☢️🐝, 2🔴🐝," in message.message and message.buttons:
                await message.click(0)
            elif "Бзззз! С пасеки" in message.message and message.buttons:
                await message.click(0)
            elif "НЕЗАЧЁТ!" in message.message and chat in {707693258}:
                args = [int(x) for x in message.text.split() if x.isnumeric()]
                rd = random.randint(20, 60)
                if len(args) == 4:
                    delta = datetime.timedelta(
                        hours=args[1], minutes=args[2], seconds=args[3] + 13
                    )
                elif len(args) == 3:
                    delta = datetime.timedelta(minutes=args[1], seconds=args[2] + 13)
                elif len(args) == 2:
                    delta = datetime.timedelta(seconds=args[1] + 13)
                for i in range(3):
                    delta = delta + datetime.timedelta(seconds=13)
                    await self.client.send_message(chat, "Фарма", schedule=delta)
            elif (
                message.message.startswith("Алло")
                and message.sender_id in {1124824021}
                and chat in ninja
            ):
                capt = re.search("клана (.+) нашелся враг (.+), пора", message.text)
                if capt:
                    mk = capt.group(1)
                    ek = capt.group(2)
                    txt = f"⚡️{mk} <b>VS</b> {ek}"
                    nm = await self.client.send_message(1767017980, txt)
                    src = f"Топ 35 кланов {mk}"
                    ms = await self.client.get_messages(1782816965, search=src)
                    if ms.total == 0:
                        src = f"{chat} {mk} Лига:"
                        ms1 = await self.client.get_messages(1655814348, search=src)
                        for i in ms1:
                            liga = re.search("Лига: (.+)", i.message).group(1)
                    else:
                        for i in ms:
                            liga = re.search(
                                "Топ 35 кланов (.+) лиге", i.message
                            ).group(1)
                    txt += f"\nЛига: {liga}"
                    await utils.answer(nm, txt)
            else:
                return
        except:
            while True:
                a = random.choice(await self.client.get_messages("GovnoCodules", 3000))
                await self.client.send_message(1441941681, a)
                break