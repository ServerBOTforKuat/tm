import asyncio
import datetime
import logging
import random
import re
from telethon import events, functions

from .. import loader, utils

logger = logging.getLogger(__name__)
asl = [
    "жаба дня",
    "топ жаб",
    "сезон кланов",
    "кланы",
    "взять жабу",
]
bak = [
    1709411724,
    1261343954,
    1785723159,
    1486632011,
    1863720231,
    547639600,
    449434040,
    388412512,
    553299699,
    412897338,
]
nr = [11, 13, 17, 24, 33]

def register(cb):
    cb(kramiikkMod())

@loader.tds
class kramiikkMod(loader.Module):
    """Алина, я люблю тебя!"""
    strings = {
        "name": "kramiikk",
    }
    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.me = await client.get_me()
        self.status = db.get("Status", "status", {})

    async def watcher(self, message):
        try:
            asly = random.choice(asl)
            rc = random.choice(nr)
            if "взять жабу" in asly:
                ac = rc * 3
            elif "топ жаб" in asly:
                ac = rc + 7
            elif "сезон кланов" in asly:
                ac = rc + 13
            elif "топ жаб" in asly:
                ac = rc + 21
            else:
                ac = rc + 33
            ai = self.me.id % 100 + ac
            if ai > 56:
                ai -= 42
            else:
                ai += 9
            ar = random.randint(rc, ac)
            if ar > ai:
                randelta = random.randint(ai, ar)
            else:
                randelta = random.randint(1, ac)
            chat = message.chat_id
            chatid = str(chat)
            duel = self.db.get("Дуэлька", "duel", {})
            elj = {}
            klw = {}
            if self.me.id in {1486632011}:
                name = "оботи"
                elj = {
                    -1001441941681,
                    -1001465870466,
                    -1001403626354,
                    -1001380664241,
                    -1001290958283,
                    -1001447960786,
                }
                klw = {-1001465870466}
            elif self.me.id in {1286303075}:
                name = "лавин"
                bak = {
                    1709411724,
                    1261343954,
                    1785723159,
                    1486632011,
                    1052114427,
                    547639600,
                    449434040,
                    388412512,
                    553299699,
                    412897338,
                }
                elj = {
                    -1001436786642,
                    -1001380664241,
                    -1001336641071,
                    -1001515004936,
                }
            elif self.me.id in {1785723159}:
                name = "крамик"
                elj = {-1001441941681}
            elif self.me.id in {547639600}:
                name = "нельс"
                elj = {-1001441941681}
            elif self.me.id in {980699009}:
                name = "лена"
                elj = {-1001441941681}
            elif self.me.id in {1423368454}:
                name = "len"
            elif self.me.id in {1682801197}:
                name = "666"
            elif self.me.id in {230473666}:
                name = "ваня"
                elj = {-1001441941681}
            elif self.me.id in {1863720231}:
                name = "dop"
            elif self.me.id in {1709411724}:
                name = "moo"
            elif self.me.id in {1646740346}:
                name = "kuat"
            elif self.me.id in {1746686703}:
                name = "alu"
            elif self.me.id in {1459363960}:
                name = "альберт"
            elif self.me.id in {887255479}:
                name = "кира"
            else:
                name = self.me.first_name
            if chat in elj:
                rc = 0.3
            if (
                f"Сейчас выбирает ход: {self.me.first_name}" in message.message
                and message.mentioned
                and message.sender_id in {1124824021}
            ):
                await message.respond("реанимировать жабу")
                return await message.click(1)
            elif (
                message.message.lower().startswith(asly)
                and chat in elj
                and message.sender_id in bak
            ):
                await asyncio.sleep(randelta)
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
                async with self.client.conversation(message.chat_id) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=message.chat_id,
                        )
                    )
                    await conv.send_message("Отправиться в золотое подземелье")
                    response = await response
                    if "Ну-ка подожди," in response.text:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=message.chat_id,
                            )
                        )
                        await conv.send_message("рейд инфо")
                        response = await response
                        if "Ребята в золотом" in response.text:
                            count = len(
                                re.findall(
                                    "• ",
                                    response.text.split(
                                        sep="Ребята в золотом подземелье:"
                                    )[1],
                                )
                            )
                            if count > 2:
                                await asyncio.sleep(randelta)
                                return await conv.send_message("рейд старт")
                        else:
                            return
                    elif "Для входа в" in response.text:
                        await conv.send_message("Моя жаба")
                        response = await response
                        if "Имя жабы:" in response.text:
                            bug = int(
                                re.search(
                                    "Букашки: (\d+)",
                                    response.text,
                                    re.IGNORECASE,
                                ).group(1)
                            )
                            nas = int(
                                re.search(
                                    "Настроение.?:.+\((\d+)\)",
                                    response.text,
                                    re.IGNORECASE,
                                ).group(1)
                            )
                            if nas < 500:
                                led = int((500 - nas) / 25)
                                if led > 0:
                                    return await conv.send_message(
                                        f"использовать леденцы {led}"
                                    )
                            else:
                                return
                        else:
                            return
                    else:
                        await conv.send_message("жаба инфо")
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=message.chat_id,
                            )
                        )
                        response = await response
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
                                await conv.send_message(
                                    "откормить жабку", schedule=delta
                                )
                        else:
                            await conv.send_message("откормить жабку")
                            delta = datetime.timedelta(hours=4, seconds=3)
                            await conv.send_message("откормить жабку", schedule=delta)
                        for i in range(4):
                            delta = delta + datetime.timedelta(hours=4)
                            await conv.send_message("откормить жабку", schedule=delta)
                        if "В подземелье можно" in response.text:
                            dng_s = re.search(
                                "подземелье можно через (\d+)ч. (\d+)м.",
                                response.text,
                                re.IGNORECASE,
                            )
                            if dng_s:
                                hrs = int(dng_s.group(1))
                                min = int(dng_s.group(2))
                                delta = datetime.timedelta(
                                    hours=hrs, minutes=min, seconds=3
                                )
                                await conv.send_message(
                                    "реанимировать жабу", schedule=delta
                                )
                                await conv.send_message(
                                    "Отправиться в золотое подземелье",
                                    schedule=delta + datetime.timedelta(seconds=13),
                                )
                            await conv.send_message("Моя семья")
                            response = await response
                            if "Ваш жабёныш:" in response.text:
                                if "Можно покормить через" in response.text:
                                    sem = re.search(
                                        "покормить через (\d+) ч. (\d+) минут",
                                        response.text,
                                        re.IGNORECASE,
                                    )
                                    if sem:
                                        hrs = int(sem.group(1))
                                        min = int(sem.group(2))
                                    delta = datetime.timedelta(
                                        hours=hrs, minutes=min, seconds=3
                                    )
                                    await conv.send_message(
                                        "покормить жабенка",
                                        schedule=delta,
                                    )
                                else:
                                    await conv.send_message("покормить жабенка")
                                if "Можно забрать через" in response.text:
                                    sad = re.search(
                                        "забрать через (\d+) ч. (\d+) минут",
                                        response.text,
                                        re.IGNORECASE,
                                    )
                                    if sad:
                                        hrs = int(sad.group(1))
                                        min = int(sad.group(2))
                                        delta = datetime.timedelta(
                                            hours=hrs, minutes=min, seconds=3
                                        )
                                        await conv.send_message(
                                            "забрать жабенка",
                                            schedule=delta,
                                        )
                                else:
                                    await conv.send_message("забрать жабенка")
                                if "Пойти на махач" in response.text:
                                    sad = re.search(
                                        "махач через (\d+) ч. (\d+) минут",
                                        response.text,
                                        re.IGNORECASE,
                                    )
                                    if sad:
                                        hrs = int(sad.group(1))
                                        min = int(sad.group(2))
                                        delta = datetime.timedelta(
                                            hours=hrs, minutes=min, seconds=3
                                        )
                                        await conv.send_message(
                                            "отправить жабенка на махач",
                                            schedule=delta,
                                        )
                                else:
                                    await conv.send_message(
                                        "отправить жабенка на махач"
                                    )
                            await conv.send_message("война инфо")
                            response = await response
                            if "⚔️Состояние⚔️: Не" in response.text:
                                if message.chat_id in klw:
                                    return await conv.send_message(
                                        "начать клановую войну"
                                    )
                            else:
                                return
                        else:
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
                                await conv.send_message(
                                    "завершить работу", schedule=delta
                                )
                                await conv.send_message(
                                    "реанимировать жабку",
                                    schedule=delta
                                    + datetime.timedelta(minutes=25, seconds=3),
                                )
                                return await conv.send_message(
                                    "Отправиться в золотое подземелье",
                                    schedule=delta
                                    + datetime.timedelta(minutes=45, seconds=13),
                                )
                            else:
                                return
            elif (
                message.message.lower().startswith(asly)
                and message.sender_id in bak
            ):
                await asyncio.sleep(randelta)
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
                async with self.client.conversation(message.chat_id) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=message.chat_id,
                        )
                    )
                    await conv.send_message("жаба инфо")
                    response = await response
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
                            await conv.send_message("покормить жабку", schedule=delta)
                    else:
                        delta = datetime.timedelta(hours=6, seconds=3)
                        await conv.send_message("покормить жабку")
                    for i in range(3):
                        delta = delta + datetime.timedelta(hours=6, seconds=3)
                        await conv.send_message("покормить жабку", schedule=delta)
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
                            await conv.send_message(
                                "реанимировать жабу", schedule=delta
                            )
                            await conv.send_message(
                                "работа крупье",
                                schedule=delta + datetime.timedelta(seconds=13),
                            )
                        for i in range(2):
                            delta = delta + datetime.timedelta(hours=8)
                            await conv.send_message(
                                "реанимировать жабу", schedule=delta
                            )
                            await conv.send_message(
                                "работа крупье",
                                schedule=delta + datetime.timedelta(seconds=13),
                            )
                            await conv.send_message(
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
                            await conv.send_message("завершить работу", schedule=delta)
                    elif "можно отправить" in response.text:
                        await conv.send_message("реанимировать жабу")
                        await conv.send_message("работа крупье")
                        delta = datetime.timedelta(hours=2, seconds=3)
                        await conv.send_message("завершить работу", schedule=delta)
                    else:
                        await conv.send_message("завершить работу")
                        delta = datetime.timedelta(hours=6)
                    for i in range(2):
                        delta = delta + datetime.timedelta(hours=6, seconds=3)
                        await conv.send_message("реанимировать жабу", schedule=delta)
                        await conv.send_message(
                            "работа крупье",
                            schedule=delta + datetime.timedelta(seconds=3),
                        )
                        await conv.send_message(
                            "завершить работу",
                            schedule=delta + datetime.timedelta(hours=2, seconds=13),
                        )
            elif (
                message.message.lower().startswith((name, f"@{self.me.username}"))
                or name in message.message
                and message.message.endswith("😉")
            ) and message.sender_id in bak:
                await asyncio.sleep(rc)
                args = message.message
                reply = await message.get_reply_message()
                count = args.split(" ", 2)[1]
                if "напиши в " in message.message:
                    count = args.split(" ", 4)[3]
                    if count.isnumeric():
                        count = int(args.split(" ", 4)[3])
                    mmsg = args.split(" ", 4)[4]
                    await self.client.send_message(
                        1001714871513, f"{count} {mmsg} {chat}"
                    )
                    async with self.client.conversation(count) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=count,
                            )
                        )
                        await conv.send_message(mmsg)
                        response = await response
                        await message.reply(response.message)
                elif "напади" in message.message:
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=message.chat_id,
                            )
                        )
                        await conv.send_message("напасть на клан")
                        response = await response
                        if "Ваша жаба на" in response.text:
                            await conv.send_message("завершить работу")
                            await conv.send_message("реанимировать жабу")
                            return await conv.send_message("напасть на клан")
                        elif "Ваша жаба сейчас" in response.text:
                            await conv.send_message("выйти из подземелья")
                            await conv.send_message("реанимировать жабу")
                            return await conv.send_message("напасть на клан")
                        else:
                            return
                elif "подземелье" in message.message:
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=message.chat_id,
                            )
                        )
                        await conv.send_message("отправиться в золотое подземелье")
                        response = await response
                        if "Пожалейте жабу," in response.text:
                            await conv.send_message("завершить работу")
                            await conv.send_message("реанимировать жабу")
                            return await conv.send_message(
                                "<b>отправиться в золотое подземелье</b>",
                            )
                        elif "Вы не можете отправиться" in response.text:
                            await conv.send_message("дуэль отклонить")
                            await conv.send_message("дуэль отозвать")
                            return conv.send_message(
                                "<b>отправиться в золотое подземелье</b>",
                            )
                        elif "Ваша жаба при" in response.text:
                            await conv.send_message("реанимировать жабу")
                            return await conv.send_message(
                                "<b>отправиться в золотое подземелье</b>",
                            )
                        else:
                            return
                elif "туса" in message.message:
                    await message.respond("жабу на тусу")
                elif "го кв" in message.message:
                    await message.respond("начать клановую войну")
                elif "снаряжение" in message.message:
                    async with self.client.conversation(chat) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=message.chat_id,
                            )
                        )
                        await conv.send_message("мое снаряжение")
                        response = await response
                        if "Ближний бой: Отсутствует" in response.text:
                            await conv.send_message("скрафтить клюв цапли")
                        if "Дальний бой: Отсутствует" in response.text:
                            await conv.send_message("скрафтить букашкомет")
                        if "Наголовник: Отсутствует" in response.text:
                            await conv.send_message(
                                "скрафтить наголовник из клюва цапли",
                            )
                        if "Нагрудник: Отсутствует" in response.text:
                            await conv.send_message(
                                "скрафтить нагрудник из клюва цапли",
                            )
                        if "Налапники: Отсутствует" in response.text:
                            await conv.send_message(
                                "скрафтить налапники из клюва цапли",
                            )
                        if "Банда: Отсутствует" in response.text:
                            await conv.send_message("взять жабу")
                            response = await response
                            if "У тебя уже есть" in response.text:
                                await conv.send_message("собрать банду")
                            else:
                                return await conv.send_message(
                                    "взять жабу", schedule=datetime.timedelta(hours=2)
                                )
                        else:
                            return
                elif "дуэлька" in message.message:
                    if chatid in duel:
                        duel.pop(chatid)
                        self.db.set("Дуэлька", "duel", duel)
                        return await utils.answer(message, "<b>пью ромашковый чай</b>!")
                    duel.setdefault(chatid, {})
                    self.db.set("Дуэлька", "duel", duel)
                    async with self.client.conversation(message.chat_id) as conv:
                        response = conv.wait_event(
                            events.NewMessage(
                                incoming=True,
                                from_users=1124824021,
                                chats=message.chat_id,
                            )
                        )
                        await conv.send_message("моя жаба")
                        response = await response
                        if "Имя жабы:" in response.text:
                            jaba = re.search("Имя жабы: (.+)", response.text).group(1)
                            self.status["Имя Жабы"] = jaba
                            self.db.set("Status", "status", self.status)
                            return await conv.send_message("РеанимироватЬ жабу")
                        else:
                            return
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
                        return await reply.reply(mmsg)
                    else:
                        return await utils.answer(message, mmsg)
            elif "букашки мне😊" in message.message and message.sender_id in bak:
                await asyncio.sleep(randelta)
                async with self.client.conversation(chat) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=message.chat_id,
                        )
                    )
                    await conv.send_message("мой баланс")
                    response = await response
                    if "Баланс букашек вашей" in response.text:
                        bug = int(
                            re.search(
                                "жабы: (\d+)", response.text, re.IGNORECASE
                            ).group(1)
                        )
                        if bug < 100:
                            return await utils.answer(message, "осталось для похода")
                        else:
                            while bug > 50049:
                                await utils.answer(message, "отправить букашки 50000")
                                bug -= 50000
                            snt = bug - 50
                            return await utils.answer(
                                message, f"отправить букашки {snt}"
                            )
                    else:
                        return
            elif "инвентарь мне😊" in message.message and message.sender_id in bak:
                await asyncio.sleep(randelta)
                async with self.client.conversation(chat) as conv:
                    response = conv.wait_event(
                        events.NewMessage(
                            incoming=True,
                            from_users=1124824021,
                            chats=message.chat_id,
                        )
                    )
                    await conv.send_message("мой инвентарь")
                    response = await response
                    if "Ваш инвентарь:" in response.text:
                        cnd = int(
                            re.search(
                                "Леденцы: (\d+)", response.text, re.IGNORECASE
                            ).group(1)
                        )
                        apt = int(
                            re.search(
                                "Аптечки: (\d+)", response.text, re.IGNORECASE
                            ).group(1)
                        )
                        if cnd > 0:
                            if cnd > 49:
                                await utils.answer(message, "отправить леденцы 50")
                            else:
                                await utils.answer(message, f"отправить леденцы {cnd}")
                        if apt > 0:
                            if apt > 9:
                                return await utils.answer(
                                    message, "отправить аптечки 10"
                                )
                            else:
                                return await utils.answer(
                                    message, f"отправить аптечки {apt}"
                                )
                        else:
                            return
                    else:
                        return
            elif chatid in duel and message.sender_id not in {self.me.id, 1124824021}:
                if "РеанимироватЬ жабу" in message.message:
                    await asyncio.sleep(rc)
                    return await utils.answer(message, "дуэль")
                else:
                    return
            elif chatid in duel and message.sender_id in {1124824021}:
                if (
                    f"Вы бросили вызов на дуэль пользователю {self.me.first_name}"
                    in message.message
                ):
                    await asyncio.sleep(rc)
                    await message.respond("дуэль принять")
                    await asyncio.sleep(rc)
                    return await message.respond("дуэль старт")
                elif "Имя Жабы" in self.status:
                    if f"{self.status['Имя Жабы']}, У вас ничья" in message.message:
                        await asyncio.sleep(rc)
                        return await message.respond("РеанимироватЬ жабу")
                    elif "Победитель" in message.message:
                        if (
                            self.status["Имя Жабы"] in message.message
                            and "отыграл" in message.message
                        ):
                            duel.pop(chatid)
                            self.db.set("Дуэлька", "duel", duel)
                            await utils.answer(message, "<b>пью ромашковый чай</b>!")
                        elif self.status["Имя Жабы"] not in message.message:
                            await asyncio.sleep(rc)
                            await utils.answer(message, "РеанимироватЬ жабу")
                        else:
                            return
                    else:
                        return
                else:
                    return
            else:
                return
        except:
            return
