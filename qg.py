__version__ = (1, 1, 0)

# scope: inline_content
# meta developer: @kramiikk
import logging
from asyncio import sleep

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Message

from .. import loader  # noqa

try:
    from .. import utils  # noqa
    from ..inline import GeekInlineQuery, rand  # noqa
except ImportError:
    from .. import utils  # noqa
    from ..inline.types import GeekInlineQuery  # noqa
    from ..utils import rand  # noqa

logger = logging.getLogger(__name__)

ua = [
    "all",
    "Кіровоградська_область",
    "Попаснянська_територіальна_громада",
    "Бердянський_район",
    "Полтавська_область",
    "м_Краматорськ_та_Краматорська_територіальна_громада",
    "м_Старокостянтинів_та_Старокостянтинівська_територіальна_громада",
    "Ізюмський_район",
    "Покровська_територіальна_громада",
    "Волноваський_район",
    "Краматорський_район",
    "Київська_область",
    "м_Київ",
    "Херсонська_область",
    "Ніжинський_район",
    "Бахмутська_територіальна_громада",
    "м_Кремінна_та_Кремінська_територіальна_громада",
    "Рівненська_область",
    "Запорізька_область",
    "м_Маріуполь_та_Маріупольська_територіальна_громада",
    "м_Рівне_та_Рівненська_територіальна_громада",
    "м_Черкаси_та_Черкаська_територіальна_громада",
    "Марїнська_територіальна_громада",
    "Сквирська_територіальна_громада",
    "Охтирський_район",
    "м_Конотоп_та_Конотопська_територіальна_громада",
    "Вознесенський_район",
    "Сарненський_район",
    "Миколаївський_район",
    "Смілянська_територіальна_громада",
    "Сєвєродонецький_район",
    "Гірська_територіальна_громада",
    "Костянтинівська_територіальна_громада",
    "Прилуцький_район",
    "м_Пирятин_та_Пирятинська_територіальна_громада",
    "Вишгородська_територіальна_громада",
    "Воскресенська_територіальна_громада",
    "м_Переяслав_та_Переяславська_територіальна_громада",
    "м_Полтава_та_Полтавська_територіальна_громада",
    "м_Вознесенськ_та_Вознесенська_територіальна_громада",
    "Дружківська_територіальна_громада",
    "Золотоніський_район",
    "Макарівська_територіальна_громада",
    "Дубровицька_територіальна_громада",
    "Хмельницька_область",
    "Великоновосілківська_територіальна_громада",
    "м_Шостка_та_Шосткинська_територіальна_громада",
    "Львівська_область",
    "Волинська_область",
    "Первомайський_район",
    "м_Запоріжжя_та_Запорізька_територіальна_громада",
    "м_Бровари_та_Броварська_територіальна_громада",
    "Лиманська_територіальна_громада",
    "м_Лисичанськ_та_Лисичанська_територіальна_громада",
    "м_Бориспіль_та_Бориспільська_територіальна_громада",
    "м_Обухів_та_Обухівська_територіальна_громада",
    "Звенигородський_район",
    "Роздільнянський_район",
    "м_Нікополь_та_Нікопольська_територіальна_громада",
    "м_Першотравенськ_та_Першотравенська_територіальна_громада",
    "м_Васильків_та_Васильківська_територіальна_громада",
    "Кропивницький_район",
    "Шепетівський_район",
    "Житомирська_область",
    "Вараський_район",
    "Болградський_район",
    "Закарпатська_область",
    "Шосткинський_район",
    "Гребінківська_територіальна_громада",
    "Чернівецька_область",
    "Синельниківський_район",
    "Уманська_територіальна_громада",
    "Олешківська_територіальна_громада",
    "м_Кременчук_та_Кременчуцька_територіальна_громада",
    "Коростенський_район",
    "Купянський_район",
    "Подільський_район",
    "м_Мелітополь_та_Мелітопольська_територіальна_громада",
    "Ізмаїльський_район",
    "Вінницька_область",
    "м_Славутич_та_Славутицька_територіальна_громада",
    "Бородянська_територіальна_громада",
    "Святогірська_територіальна_громада",
    "Добропільська_територіальна_громада",
    "Черкаський_район",
    "Пологівський_район",
    "м_Сарни_та_Сарненська_територіальна_громада",
    "Маріупольський_район",
    "Лозівський_район",
    "Березівський_район",
    "Українська_територіальна_громада",
    "м_Охтирка_та_Охтирська_територіальна_громада",
    "Жашківська_територіальна_громада",
    "Житомирський_район",
    "Донецький_район",
    "м_Кривий_Ріг_та_Криворізька_територіальна_громада",
    "Радомишльська_територіальна_громада",
    "м_Дніпро_та_Дніпровська_територіальна_громада",
    "м_Миколаїв_та_Миколаївська_територіальна_громада",
    "Гостомелська_територіальна_громада",
    "м_Миргород_та_Миргородська_територіальна_громада",
    "Сумська_область",
    "Торецька_територіальна_громада",
    "м_Ватутіне_та_Ватутінська_територіальна_громада",
    "м_Коростень_та_Коростенська_територіальна_громада",
    "Харківський_район",
    "Уманський_район",
    "Сумський_район",
    "Одеський_район",
    "БілгородДністровський_район",
    "Тернопільська_область",
    "Первомайська_територіальна_громада",
    "м_Первомайськ_та_Первомайська_територіальна_громада",
    "Чугуївський_район",
    "м_Фастів_та_Фастівська_територіальна_громада",
    "Миронівська_територіальна_громада",
    "м_Лубни_та_Лубенська_територіальна_громада",
    "Черкаська_область",
    "Луганська_область",
    "м_Житомир_та_Житомирська_територіальна_громада",
    "Новоукраїнський_район",
    "м_Словянськ_та_Словянська_територіальна_громада",
    "Чернігівський_район",
    "м_Очаків_та_Очаківська_територіальна_громада",
    "Вугледарська_територіальна_громада",
    "м_Сєвєродонецьк_та_Сєвєродонецька_територіальна_громада",
    "Дніпропетровська_область",
    "Запорізький_район",
    "Широківська_територіальна_громада",
    "Узинська_територіальна_громада",
    "Миколаївська_область",
    "Харківська_область",
    "НовоградВолинський_район",
    "Курахівська_територіальна_громада",
    "м_Рубіжне_та_Рубіжанська_територіальна_громада",
    "Донецька_область",
    "м_Суми_та_Сумська_територіальна_громада",
    "м_Біла_Церква_та_Білоцерківська_територіальна_громада",
    "Голованівський_район",
    "Одеська_область",
    "Павлоградський_район",
    "Чернігівська_область",
    "Сватівський_район",
    "ІваноФранківська_область",
    "Покровський_район",
    "Бахмутський_район",
]


class AirMod(loader.Module):
    """🇺🇦 Предупреждение о воздушной тревоге.
    Нужно быть подписаным на @air_alert_ua и включены уведомления в вашем боте"""

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client
        self.regions = db.get("AirAlert", "regions", [])
        self.bot_id = (await self.inline.bot.get_me()).id
        self.forwards = db.get("AirAlert", "forwards", [])
        self.me = (await client.get_me()).id
        try:
            await client(
                JoinChannelRequest(await self.client.get_entity("t.me/air_alert_ua"))
            )
        except Exception:
            logger.error("Can't join t.me/air_alert_ua")
        try:
            await client(JoinChannelRequest(await self.client.get_entity("t.me/x69xy")))
        except Exception:
            logger.error(f"Can't join t.me/x69xy")
        try:
            post = (await client.get_messages("t.me/x69xy", ids=[2]))[0]
            await post.react("🔥")
        except Exception:
            logger.error("Can't react to t.me/x69xy")

    async def alertforwardcmd(self, message: Message) -> None:
        """Перенаправление предупреждений в другие чаты. Для добавления/удаления введите команду с ссылкой на чат.
        Для просмотра чатов введите команду без аргументов"""
        text = utils.get_args_raw(message)
        if not text:
            chats = "<b>Текущие чаты для перенаправления: </b>"
            for chat in self.forwards:
                chats += f"\n{chat}"
            return await utils.answer(message, chats)
        chat = int(text)
        if chat in self.forwards:
            self.forwards.remove(chat)
            self.db.set("AirAlert", "forwards", self.forwards)
            await utils.answer(message, "<b>Чат успешно удален для перенаправления</b>")
        else:
            self.forwards.append(chat)
            self.db.set("AirAlert", "forwards", self.forwards)
            await utils.answer(
                message, "<b>Чат успешно установлен для перенаправления</b>"
            )

    async def alert_inline_handler(self, query: GeekInlineQuery) -> None:
        """Выбор регионов.
        Чтобы получать все предупреждения введите alert all.
        Чтобы посмотреть ваши регионы alert my"""
        text = query.args
        if not text:
            result = ua
        elif text == "my":
            result = self.regions
        else:
            result = [region for region in ua if text.lower() in region.lower()]
        if not result:
            await query.e404()
            return
        res = [
            InlineQueryResultArticle(
                id=rand(20),
                title=f"{'✅' if reg in self.regions else '❌'}{reg if reg != 'all' else 'Все уведомления'}",
                description=f"Нажмите чтобы {'удалить' if reg in self.regions else 'добавить'}"
                if reg != "all"
                else f"🇺🇦 Нажмите чтобы {'выключить' if 'all' in self.regions else 'включить'} все уведомления",
                input_message_content=InputTextMessageContent(
                    f"⌛ Редактирование региона <code>{reg}</code>",
                    parse_mode="HTML",
                ),
            )
            for reg in result[:50]
        ]
        await query.answer(res, cache_time=0)

    async def watcher(self, message: Message) -> None:
        if (
            getattr(message, "out", False)
            and getattr(message, "via_bot_id", False)
            and message.via_bot_id == self.bot_id
            and "⌛ Редактирование региона" in getattr(message, "raw_text", "")
        ):
            self.regions = self.db.get("AirAlert", "regions", [])
            region = message.raw_text[25:]
            state = "добавлен"
            if region not in self.regions:
                self.regions.append(region)
            else:
                self.regions.remove(region)
                state = "удален"
            self.db.set("AirAlert", "regions", self.regions)
            try:
                e = await self.client.get_entity("t.me/air_alert_ua")
                sub = not e.left
            except Exception:
                sub = False
            n = "\n"
            res = f"<b>Регион <code>{region}</code> успешно {state}</b>{n}"
            if not sub:
                res += (
                    "<b>НЕ ВЫХОДИ С @air_alert_ua (иначе ничего работать не будет)</b>"
                )
                await self.client(
                    JoinChannelRequest(
                        await self.client.get_entity("t.me/air_alert_ua")
                    )
                )
            await self.inline.form(res, message=message)
        if (
            getattr(message, "peer_id", False)
            and getattr(message.peer_id, "channel_id", 0) == 1766138888
            and (
                "all" in self.regions
                or any(reg in message.raw_text for reg in self.regions)
            )
        ):
            for _ in range(3):
                await self.inline.bot.send_message(
                    self.me, message.text, parse_mode="HTML"
                )
                await sleep(1)
            for chat in self.forwards:
                await self.client.send_message(chat, message.text)
        return


# @loader.tds
# class FbackMod(loader.Module):
#     """yoooh"""

#     __metaclass__ = abc.ABCMeta

#     strings = {
#         "name": "Fback",
#         "/start": "🤵‍♀️ <b>Привет. Это бот обратной связи с {}. Прочитайте /note, прежде чем продолжить.</b>\n<b>Вы можете отправлять только одно сообщение в минуту.</b>",
#         "/note": (
#             "👨‍🎓 <b><u>Правила общения в Интернете:</u></b>\n\n"
#             "🚫 <b>Не <u>пишите</u> просто 'Привет'</b>\n"
#             "🚫 <b>Не <u>отправляйте</u> рекламу</b>\n"
#             "🚫 <b>Не <u>адресуйте</u> оскорбления</b>\n"
#             "✅ <b>Отправьте послание одним сообщением</b>"
#         ),
#         "enter": "✍️ <b>Отлично, можете отправить сообщение</b>",
#         "sent": "✅ <b>Ваше сообщение отправлено</b>",
#     }

#     async def inline__close(self, call: CallbackQuery) -> None:
#         await call.delete()

#     def get(self, *args) -> dict:
#         return self._db.get(self.strings["name"], *args)

#     def set(self, *args) -> None:
#         return self._db.set(self.strings["name"], *args)

#     async def coin_inline_handler(self, query: InlineQuery) -> None:
#         """
#         Heads or tails?
#         @allow: all
#         """

#         r = "🦅 Heads" if randint(0, 1) else "🪙 Tails"
#         await query.answer(
#             [
#                 InlineQueryResultArticle(
#                     id=utils.rand(20),
#                     title="Toss a coin",
#                     description="Trust in the God of luck, and he will be by your side!",
#                     input_message_content=InputTextMessageContent(
#                         f"<i>The God of luck tells us...</i> <b>{r}</b>",
#                         "HTML",
#                         disable_web_page_preview=True,
#                     ),
#                     thumb_url="https://img.icons8.com/external-justicon-flat-justicon/64/000000/external-coin-pirates-justicon-flat-justicon-1.png",
#                     thumb_width=128,
#                     thumb_height=128,
#                 )
#             ],
#             cache_time=0,
#         )

#     async def random_inline_handler(self, query: InlineQuery) -> None:
#         """
#         [number] - Send random number less than specified
#         @allow: all
#         """

#         if not query.args:
#             return

#         a = query.args

#         if not str(a).isdigit():
#             return

#         await query.answer(
#             [
#                 InlineQueryResultArticle(
#                     id=utils.rand(20),
#                     title=f"Toss random number less or equal to {a}",
#                     description="Trust in the God of luck, and he will be by your side!",
#                     input_message_content=InputTextMessageContent(
#                         f"<i>The God of luck screams...</i> <b>{randint(1, int(a))}</b>",
#                         "HTML",
#                         disable_web_page_preview=True,
#                     ),
#                     thumb_url="https://img.icons8.com/external-flaticons-flat-flat-icons/64/000000/external-numbers-auction-house-flaticons-flat-flat-icons.png",
#                     thumb_width=128,
#                     thumb_height=128,
#                 )
#             ],
#             cache_time=0,
#         )

#     async def choice_inline_handler(self, query: InlineQuery) -> None:
#         """
#         Make a choice
#         @allow: all
#         """

#         if not query.args or not query.args.count("|"):
#             return

#         args = query.args
#         text = args.split("|")
#         words = text[1]
#         text1 = text[0].split(" ")
#         time = int(text1[0]) * 60
#         words1 = " ".join(text1[1:])

#         await query.answer(
#             [
#                 InlineQueryResultArticle(
#                     id=utils.rand(20),
#                     title="Choose one item from list",
#                     description="Trust in the God of luck, and he will be by your side!",
#                     input_message_content=InputTextMessageContent(
#                         f"<i>The God of luck whispers...</i> <b>{words1}</b>",
#                         "HTML",
#                         disable_web_page_preview=True,
#                     ),
#                     thumb_url="https://img.icons8.com/external-filled-outline-geotatah/64/000000/external-choice-customer-satisfaction-filled-outline-filled-outline-geotatah.png",
#                     thumb_width=128,
#                     thumb_height=128,
#                 )
#             ],
#             cache_time=0,
#         )
#         await asyncio.sleep(time)
#         await query.edit(words)

#     async def client_ready(self, client, db) -> None:
#         self._db = db
#         self._client = client
#         self._me = (await client.get_me()).id
#         self._name = utils.escape_html(get_display_name(await client.get_me()))

#         self._bot = self.inline._bot
#         self._ratelimit = {}
#         self._markup = InlineKeyboardMarkup()
#         self._markup.add(
#             InlineKeyboardButton("✍️ Нажмите чтобы написать", callback_data="leave")
#         )

#         self._cancel = InlineKeyboardMarkup()
#         self._cancel.add(InlineKeyboardButton("🚫 Отмена", callback_data="cancel"))

#         self.__doc__ = f"Your feeback link: t.me/{self.inline._bot_username}?start\n"

#     async def aiogram_watcher(self, message: AiogramMessage) -> None:
#         if message.text == "/start":
#             await message.answer(
#                 self.strings("/start").format(self._name), reply_markup=self._markup
#             )
#         elif message.text == "/note":
#             await message.answer(self.strings("/note"), reply_markup=self._markup)
#         elif self.inline.gs(message.from_user.id) == "send":
#             await self._bot.forward_message(
#                 self._me, message.chat.id, message.message_id
#             )
#             await message.answer(self.strings("sent"))
#             self._ratelimit[message.from_user.id] = time.time() + 60
#             self.inline.ss(message.from_user.id, False)

#     async def feedback_callback_handler(self, call: CallbackQuery) -> None:
#         """
#         Handles button clicks
#         @allow: all
#         """
#         if call.data == "cancel":
#             self.inline.ss(call.from_user.id, False)
#             await self._bot.delete_message(
#                 call.message.chat.id, call.message.message_id
#             )
#             return

#         if call.data != "leave":
#             return

#         if (
#                 call.from_user.id in self._ratelimit
#                 and self._ratelimit[call.from_user.id] > time.time()
#         ):
#             await call.answer(
#                 f"Сообщение можно отправить через {self._ratelimit[call.from_user.id] - time.time():.0f} секунд",
#                 show_alert=True,
#             )
#             return

#         self.inline.ss(call.from_user.id, "send")
#         await self._bot.edit_message_text(
#             chat_id=call.message.chat.id,
#             message_id=call.message.message_id,
#             text=self.strings("enter"),
#             parse_mode="HTML",
#             disable_web_page_preview=True,
#             reply_markup=self._cancel,
#         )
