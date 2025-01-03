"""
В данном модуле написан Telegram бот.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vertex import Vertex
import re
import os
import time
import random
import string
import psutil
import telebot
import logging
import json
from os.path import exists
from telebot.types import InlineKeyboardMarkup as K, InlineKeyboardButton as B, Message, CallbackQuery, BotCommand, ReplyKeyboardRemove
from tg_bot import utils, static_keyboards as skb, keyboards as kb, CBT
from Utils import vertex_tools
import tg_bot.CBT
from locales.localizer import Localizer

logger = logging.getLogger("TGBot")
localizer = Localizer()
_ = localizer.translate
telebot.apihelper.ENABLE_MIDDLEWARE = True


class TGBot:
    def __init__(self, vertex: Vertex):
        self.vertex = vertex
        self.bot = telebot.TeleBot(self.vertex.MAIN_CFG["Telegram"]["token"], parse_mode="HTML",
                                   allow_sending_without_reply=True, num_threads=5)

        self.file_handlers = {}  # хэндлеры, привязанные к получению файла.
        self.attempts = {}  # {user_id: attempts} - попытки авторизации в Telegram ПУ.
        self.init_messages = []  # [(chat_id, message_id)] - список сообщений о запуске TG бота.

        # {
        #     chat_id: {
        #         user_id: {
        #             "state": "state",
        #             "data": { ... },
        #             "mid": int
        #         }
        #     }
        # }
        self.user_states = {}

        # {
        #    chat_id: {
        #        utils.NotificationTypes.new_message: bool,
        #        utils.NotificationTypes.new_order: bool,
        #        ...
        #    },
        # }
        #
        self.notification_settings = utils.load_notification_settings()  # настройки уведомлений.
        self.answer_templates = utils.load_answer_templates()  # заготовки ответов.
        self.authorized_users = utils.load_authorized_users()  # авторизированные пользователи.

        self.commands = {
            "menu": _("cmd_menu"),
            "profile": _("cmd_profile"),
            "test_lot": _("cmd_test_lot"),
            "upload_img": _("cmd_upload_img"),
            "ban": _("cmd_ban"),
            "unban": _("cmd_unban"),
            "black_list": _("cmd_black_list"),
            "watermark": _("cmd_watermark"),
            "logs": _("cmd_logs"),
            "del_logs": _("cmd_del_logs"),
            "about": _("cmd_about"),
            "sys": _("cmd_sys"),
            "old_orders": _("cmd_old_orders"),
            "keyboard": _("cmd_keyboard"),
            "change_cookie": _("cmd_change_cookie"),
            "restart": _("cmd_restart"),
            "power_off": _("cmd_power_off")
        }
        self.__default_notification_settings = {
            utils.NotificationTypes.ad: 1,
            utils.NotificationTypes.announcement: 1
        }

    # User states
    def get_state(self, chat_id: int, user_id: int) -> dict | None:
        """
        Получает текущее состояние пользователя.

        :param chat_id: id чата.
        :param user_id: id пользователя.

        :return: данные состояния пользователя.
        """
        try:
            return self.user_states[chat_id][user_id]
        except KeyError:
            return None

    def set_state(self, chat_id: int, message_id: int, user_id: int, state: str, data: dict | None = None):
        """
        Устанавливает состояние для пользователя.

        :param chat_id: id чата.
        :param message_id: id сообщения, после которого устанавливается данное состояние.
        :param user_id: id пользователя.
        :param state: состояние.
        :param data: доп. данные.
        """
        if chat_id not in self.user_states:
            self.user_states[chat_id] = {}
        self.user_states[chat_id][user_id] = {"state": state, "mid": message_id, "data": data or {}}

    def clear_state(self, chat_id: int, user_id: int, del_msg: bool = False) -> int | None:
        """
        Очищает состояние пользователя.

        :param chat_id: id чата.
        :param user_id: id пользователя.
        :param del_msg: удалять ли сообщение, после которого было обозначено текущее состояние.

        :return: ID сообщения-инициатора или None, если состояние и так было пустое.
        """
        try:
            state = self.user_states[chat_id][user_id]
        except KeyError:
            return None

        msg_id = state.get("mid")
        del self.user_states[chat_id][user_id]
        if del_msg:
            try:
                self.bot.delete_message(chat_id, msg_id)
            except:
                pass
        return msg_id

    def check_state(self, chat_id: int, user_id: int, state: str) -> bool:
        """
        Проверяет, является ли состояние указанным.

        :param chat_id: id чата.
        :param user_id: id пользователя.
        :param state: состояние.

        :return: True / False
        """
        try:
            return self.user_states[chat_id][user_id]["state"] == state
        except KeyError:
            return False

    # Notification settings
    def is_notification_enabled(self, chat_id: int | str, notification_type: str) -> bool:
        """
        Включен ли указанный тип уведомлений в указанном чате?

        :param chat_id: ID Telegram чата.
        :param notification_type: тип уведомлений.
        """
        try:
            return bool(self.notification_settings[str(chat_id)][notification_type])
        except KeyError:
            return False

    def toggle_notification(self, chat_id: int, notification_type: str) -> bool:
        """
        Переключает указанный тип уведомлений в указанном чате и сохраняет настройки уведомлений.

        :param chat_id: ID Telegram чата.
        :param notification_type: тип уведомлений.

        :return: вкл / выкл указанный тип уведомлений в указанном чате.
        """
        chat_id = str(chat_id)
        if chat_id not in self.notification_settings:
            self.notification_settings[chat_id] = {}

        self.notification_settings[chat_id][notification_type] = not self.is_notification_enabled(chat_id, notification_type)
        utils.save_notification_settings(self.notification_settings)
        return self.notification_settings[chat_id][notification_type]

    # handler binders
    def is_file_handler(self, m: Message):
        return self.get_state(m.chat.id, m.from_user.id) and m.content_type in ["photo", "document"]

    def file_handler(self, state, handler):
        self.file_handlers[state] = handler

    def run_file_handlers(self, m: Message):
        if (state := self.get_state(m.chat.id, m.from_user.id)) is None \
                or state["state"] not in self.file_handlers:
            return
        try:
            self.file_handlers[state["state"]](m)
        except:
            logger.error(_("log_tg_handler_error"))
            logger.debug("TRACEBACK", exc_info=True)

    def msg_handler(self, handler, **kwargs):
        """
        Регистрирует хэндлер, срабатывающий при новом сообщении.

        :param handler: хэндлер.
        :param kwargs: аргументы для хэндлера.
        """
        bot_instance = self.bot

        @bot_instance.message_handler(**kwargs)
        def run_handler(message: Message):
            try:
                handler(message)
            except:
                logger.error(_("log_tg_handler_error"))
                logger.debug("TRACEBACK", exc_info=True)

    def cbq_handler(self, handler, func, **kwargs):
        """
        Регистрирует хэндлер, срабатывающий при новом callback'е.

        :param handler: хэндлер.
        :param func: функция-фильтр.
        :param kwargs: аргументы для хэндлера.
        """
        bot_instance = self.bot

        @bot_instance.callback_query_handler(func, **kwargs)
        def run_handler(call: CallbackQuery):
            try:
                handler(call)
            except:
                logger.error(_("log_tg_handler_error"))
                logger.debug("TRACEBACK", exc_info=True)

    def mdw_handler(self, handler, **kwargs):
        """
        Регистрирует промежуточный хэндлер.

        :param handler: хэндлер.
        :param kwargs: аргументы для хэндлера.
        """
        bot_instance = self.bot

        @bot_instance.middleware_handler(**kwargs)
        def run_handler(bot, update):
            try:
                handler(bot, update)
            except:
                logger.error(_("log_tg_handler_error"))
                logger.debug("TRACEBACK", exc_info=True)

    # Система свой-чужой 0_0
    def setup_chat_notifications(self, bot: TGBot, m: Message):
        """
        Устанавливает настройки уведомлений по умолчанию в новом чате.
        """
        if m.reply_to_message and m.reply_to_message.forum_topic_created:
            return
        if str(m.chat.id) in self.notification_settings:
            return
        if m.chat.type != "private" or m.chat.id in self.authorized_users:
            self.notification_settings[str(m.chat.id)] = self.__default_notification_settings
            utils.save_notification_settings(self.notification_settings)

    def reg_admin(self, m: Message):
        """
        Проверяет, есть ли пользователь в списке пользователей с доступом к ПУ TG.
        """
        if m.chat.type != "private" or (m.from_user.id in self.attempts and self.attempts.get(m.from_user.id) >= 5):
            return
        if m.text == self.vertex.MAIN_CFG["Telegram"]["secretKey"]:
            self.authorized_users.append(m.from_user.id)
            utils.save_authorized_users(self.authorized_users)
            if str(m.chat.id) not in self.notification_settings:
                self.notification_settings[str(m.chat.id)] = self.__default_notification_settings
                utils.save_notification_settings(self.notification_settings)
            text = _("access_granted")
            logger.warning(_("log_access_granted", m.from_user.username, m.from_user.id))
        else:
            self.attempts[m.from_user.id] = self.attempts[m.from_user.id] + 1 if m.from_user.id in self.attempts else 1
            text = _("access_denied", m.from_user.username)
            logger.warning(_("log_access_attempt", m.from_user.username, m.from_user.id))
        self.bot.send_message(m.chat.id, text)

    @staticmethod
    def ignore_unauthorized_users(c: CallbackQuery):
        """
        Игнорирует callback'и от не авторизированных пользователей.
        """
        logger.warning(_("log_click_attempt", c.from_user.username, c.from_user.id, c.message.chat.username,
                         c.message.chat.id))
        return

    # Команды
    def send_settings_menu(self, m: Message):
        """
        Отправляет основное меню настроек (новым сообщением).
        """
        self.vertex.account.get()
        self.vertex.balance = self.vertex.get_balance()
        self.bot.send_message(m.chat.id, _("desc_main"), reply_markup=kb.settings_sections(self.vertex))

    def send_profile(self, m: Message):
        """
        Отправляет статистику аккаунта.
        """
        new_msg = self.bot.send_message(m.chat.id, _("updating_profile"))
        try:
            self.vertex.account.get()
            self.vertex.balance = self.vertex.get_balance()
            self.bot.send_message(m.chat.id, utils.generate_profile_text(self.vertex),
                                  reply_markup=telebot.types.InlineKeyboardMarkup()
                                  .add(telebot.types.InlineKeyboardButton("🔄 Обновить", callback_data="update_profile"))
                                  .add(telebot.types.InlineKeyboardButton("▶️ Еще", callback_data="update_adv_profile"))
                                  )
            self.bot.delete_message(new_msg.chat.id, new_msg.id)
        except:
            self.bot.edit_message_text(_("profile_updating_error"), new_msg.chat.id, new_msg.id)
            logger.debug("TRACEBACK", exc_info=True)
            self.bot.answer_callback_query(m.id)
            return
        
    def update_profile(self, c: CallbackQuery):
        """
        Обновляет статистику аккаунта.
        """
        new_msg = self.bot.send_message(c.message.chat.id, _("updating_profile"))
        try:
            self.vertex.account.get()
            self.vertex.balance = self.vertex.get_balance()
            self.bot.edit_message_text(utils.generate_profile_text(self.vertex), c.message.chat.id,
                                c.message.id,
                                reply_markup=telebot.types.InlineKeyboardMarkup()
                                .add(telebot.types.InlineKeyboardButton("🔄 Обновить", callback_data="update_profile"))
                                .add(telebot.types.InlineKeyboardButton("▶️ Еще", callback_data="update_adv_profile"))
                                )
            self.bot.delete_message(new_msg.chat.id, new_msg.id)
        except:
            self.bot.edit_message_text(_("profile_updating_error"), new_msg.chat.id, new_msg.id)
            logger.debug("TRACEBACK", exc_info=True)
            self.bot.answer_callback_query(c.id)
            return

    def change_cookie(self, m: telebot.types.Message):
        if len(m.text.split(" ")) == 2:
            if len(m.text.split(" ")[1]) != 32:
                self.bot.send_message(m.chat.id, "Неверный формат токена. Попробуй еще раз!")
                return
            self.vertex.account.golden_key = m.text.split(" ")[1]
            self.vertex.MAIN_CFG.set("FunPay", "golden_key", m.text.split(" ")[1])
            self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")
            self.vertex.account.get(True)
            self.bot.send_message(m.chat.id, "✅ Успешно изменено перезапустите бота.")
        else:
            self.bot.send_message(m.chat.id, "Команда введена не правильно! /change_cookie [golden_key]")

    def update_adv_profile(self, c: CallbackQuery):
        """
        Обновляет дополнительную статистику аккаунта.
        """
        new_msg = self.bot.send_message(c.message.chat.id, _("updating_profile"))
        try:
            self.vertex.account.get()
            self.vertex.balance = self.vertex.get_balance()
            self.bot.edit_message_text(utils.generate_adv_profile(self.vertex), c.message.chat.id,
                                c.message.id,
                                reply_markup=telebot.types.InlineKeyboardMarkup()
                                .add(telebot.types.InlineKeyboardButton("🔄 Обновить", callback_data="update_adv_profile"))
                                .add(telebot.types.InlineKeyboardButton("◀️ Назад", callback_data="update_profile"))
                                )
            self.bot.delete_message(new_msg.chat.id, new_msg.id)
        except:
            self.bot.edit_message_text(_("profile_updating_error"), new_msg.chat.id, new_msg.id)
            logger.debug("TRACEBACK", exc_info=True)
            self.bot.answer_callback_query(c.id)
            return

    def send_orders(self, m: telebot.types.Message):
        new_mes = self.bot.send_message(m.chat.id, "Сканирую заказы (это может занять какое-то время)...")
        try:
            orders = utils.get_all_old_orders(self.vertex.account)
        except:
            self.bot.edit_message_text("❌ Не удалось получить список заказов.", new_mes.chat.id, new_mes.id)
            logger.debug("TRACEBACK", exc_info=True)
            return

        if not orders:
                self.bot.edit_message_text("❌ Просроченных заказов нет.", new_mes.chat.id, new_mes.id)
                logger.debug("TRACEBACK", exc_info=True)
                return

        orders_text = ", ".join(orders)
        text = f"Здравствуйте!\n\nПрошу подтвердить выполнение следующих заказов:\n{orders_text}\n\nЗаранее благодарю,\nС уважением."
        self.bot.edit_message_text(f"<code>{utils.escape(text)}</code>", new_mes.chat.id, new_mes.id)

    def act_manual_delivery_test(self, m: Message):
        """
        Активирует режим ввода названия лота для ручной генерации ключа теста автовыдачи.
        """
        result = self.bot.send_message(m.chat.id, _("create_test_ad_key"), reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(m.chat.id, result.id, m.from_user.id, CBT.MANUAL_AD_TEST)

    def manual_delivery_text(self, m: Message):
        """
        Генерирует ключ теста автовыдачи (ручной режим).
        """
        self.clear_state(m.chat.id, m.from_user.id, True)
        lot_name = m.text.strip()
        key = "".join(random.sample(string.ascii_letters + string.digits, 50))
        self.vertex.delivery_tests[key] = lot_name

        logger.info(_("log_new_ad_key", m.from_user.username, m.from_user.id, lot_name, key))
        self.bot.send_message(m.chat.id, _("test_ad_key_created", utils.escape(lot_name), key))

    def act_ban(self, m: Message):
        """
        Активирует режим ввода никнейма пользователя, которого нужно добавить в ЧС.
        """
        result = self.bot.send_message(m.chat.id, _("act_blacklist"), reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(m.chat.id, result.id, m.from_user.id, CBT.BAN)

    def ban(self, m: Message):
        """
        Добавляет пользователя в ЧС.
        """
        self.clear_state(m.chat.id, m.from_user.id, True)
        nickname = m.text.strip()

        if nickname in self.vertex.blacklist:
            self.bot.send_message(m.chat.id, _("already_blacklisted", nickname))
            return

        self.vertex.blacklist.append(nickname)
        vertex_tools.cache_blacklist(self.vertex.blacklist)
        logger.info(_("log_user_blacklisted", m.from_user.username, m.from_user.id, nickname))
        self.bot.send_message(m.chat.id, _("user_blacklisted", nickname))

    def act_unban(self, m: Message):
        """
        Активирует режим ввода никнейма пользователя, которого нужно удалить из ЧС.
        """
        result = self.bot.send_message(m.chat.id, _("act_unban"), reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(m.chat.id, result.id, m.from_user.id, CBT.UNBAN)

    def unban(self, m: Message):
        """
        Удаляет пользователя из ЧС.
        """
        self.clear_state(m.chat.id, m.from_user.id, True)
        nickname = m.text.strip()
        if nickname not in self.vertex.blacklist:
            self.bot.send_message(m.chat.id, _("not_blacklisted", nickname))
            return
        self.vertex.blacklist.remove(nickname)
        vertex_tools.cache_blacklist(self.vertex.blacklist)
        logger.info(_("log_user_unbanned", m.from_user.username, m.from_user.id, nickname))
        self.bot.send_message(m.chat.id, _("user_unbanned", nickname))

    def send_ban_list(self, m: Message):
        """
        Отправляет ЧС.
        """
        if not self.vertex.blacklist:
            self.bot.send_message(m.chat.id, _("blacklist_empty"))
            return
        blacklist = ", ".join(f"<code>{i}</code>" for i in self.vertex.blacklist)
        self.bot.send_message(m.chat.id, blacklist)

    def act_edit_watermark(self, m: Message):
        """
        Активирует режим ввода вотемарки сообщений.
        """
        result = self.bot.send_message(m.chat.id, _("act_edit_watermark"), reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(m.chat.id, result.id, m.from_user.id, CBT.EDIT_WATERMARK)

    def edit_watermark(self, m: Message):
        self.clear_state(m.chat.id, m.from_user.id, True)
        watermark = m.text if m.text != "-" else ""
        if re.fullmatch(r"\[[a-zA-Z]+]", watermark):
            self.bot.reply_to(m, _("watermark_error"))
            return

        self.vertex.MAIN_CFG["Other"]["watermark"] = watermark
        self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")
        if watermark:
            logger.info(_("log_watermark_changed", m.from_user.username, m.from_user.id, watermark))
            self.bot.reply_to(m, _("watermark_changed", watermark))
        else:
            logger.info(_("log_watermark_deleted", m.from_user.username, m.from_user.id))
            self.bot.reply_to(m, _("watermark_deleted"))

    def send_logs(self, m: Message):
        """
        Отправляет файл логов.
        """
        if not os.path.exists("logs/log.log"):
            self.bot.send_message(m.chat.id, _("logfile_not_found"))
        else:
            self.bot.send_message(m.chat.id, _("logfile_sending"))
            try:
                with open("logs/log.log", "r", encoding="utf-8") as f:
                    self.bot.send_document(m.chat.id, f)
            except:
                self.bot.send_message(m.chat.id, _("logfile_error"))
                logger.debug("TRACEBACK", exc_info=True)

    def del_logs(self, m: Message):
        """
        Удаляет старые лог-файлы.
        """
        deleted = 0
        for file in os.listdir("logs"):
            if not file.endswith(".log"):
                try:
                    os.remove(f"logs/{file}")
                    deleted += 1
                except:
                    continue
        self.bot.send_message(m.chat.id, _("logfile_deleted"))

    def about(self, m: Message):
        """
        Отправляет информацию о текущей версии бота.
        """
        self.bot.send_message(m.chat.id, _("about", self.vertex.VERSION))

    def send_system_info(self, m: Message):
        """
        Отправляет информацию о нагрузке на систему.
        """
        current_time = int(time.time())
        uptime = current_time - self.vertex.start_time

        ram = psutil.virtual_memory()
        cpu_usage = "\n".join(
            f"    CPU {i}:  <code>{l}%</code>" for i, l in enumerate(psutil.cpu_percent(percpu=True)))
        self.bot.send_message(m.chat.id, _("sys_info", cpu_usage, psutil.Process().cpu_percent(),
                                           ram.total // 1048576, ram.used // 1048576, ram.free // 1048576,
                                           psutil.Process().memory_info().rss // 1048576,
                                           vertex_tools.time_to_str(uptime), m.chat.id))

    def restart_vertex(self, m: Message):
        """
        Перезапускает вертекс.
        """
        self.bot.send_message(m.chat.id, _("restarting"))
        vertex_tools.restart_program()

    def ask_power_off(self, m: Message):
        """
        Просит подтверждение на отключение FPV.
        """
        self.bot.send_message(m.chat.id, _("power_off_0"), reply_markup=kb.power_off(self.vertex.instance_id, 0))

    def cancel_power_off(self, c: CallbackQuery):
        """
        Отменяет выключение (удаляет клавиатуру с кнопками подтверждения).
        """
        self.bot.edit_message_text(_("power_off_cancelled"), c.message.chat.id, c.message.id)
        self.bot.answer_callback_query(c.id)

    def power_off(self, c: CallbackQuery):
        """
        Отключает FPV.
        """
        split = c.data.split(":")
        state = int(split[1])
        instance_id = int(split[2])

        if instance_id != self.vertex.instance_id:
            self.bot.edit_message_text(_("power_off_error"), c.message.chat.id, c.message.id)
            self.bot.answer_callback_query(c.id)
            return

        if state == 6:
            self.bot.edit_message_text(_("power_off_6"), c.message.chat.id, c.message.id)
            self.bot.answer_callback_query(c.id)
            vertex_tools.shut_down()
            return

        self.bot.edit_message_text(_(f"power_off_{state}"), c.message.chat.id, c.message.id,
                                   reply_markup=kb.power_off(instance_id, state))
        self.bot.answer_callback_query(c.id)

    # Чат FunPay
    def act_send_funpay_message(self, c: CallbackQuery):
        """
        Активирует режим ввода сообщения для отправки его в чат FunPay.
        """
        split = c.data.split(":")
        node_id = int(split[1])
        try:
            username = split[2]
        except IndexError:
            username = None
        result = self.bot.send_message(c.message.chat.id, _("enter_msg_text"),  reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(c.message.chat.id, result.id, c.from_user.id,
                       CBT.SEND_FP_MESSAGE, {"node_id": node_id, "username": username})
        self.bot.answer_callback_query(c.id)

    def send_funpay_message(self, message: Message):
        """
        Отправляет сообщение в чат FunPay.
        """
        data = self.get_state(message.chat.id, message.from_user.id)["data"]
        node_id, username = data["node_id"], data["username"]
        self.clear_state(message.chat.id, message.from_user.id, True)
        response_text = message.text.strip()
        result = self.vertex.send_message(node_id, response_text, username)
        if result:
            self.bot.reply_to(message, _("msg_sent", node_id, username),
                              reply_markup=kb.reply(node_id, username, again=True, extend=True))
        else:
            self.bot.reply_to(message, _("msg_sending_error", node_id, username),
                              reply_markup=kb.reply(node_id, username, again=True, extend=True))

    def act_upload_image(self, m: Message):
        """
        Активирует режим ожидания изображения для последующей выгрузки на FunPay.
        """
        result = self.bot.send_message(m.chat.id, _("send_img"), reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(m.chat.id, result.id, m.from_user.id, CBT.UPLOAD_IMAGE)

    def act_edit_greetings_text(self, c: CallbackQuery):
        variables = ["v_date", "v_date_text", "v_full_date_text", "v_time", "v_full_time", "v_username",
                     "v_message_text", "v_chat_id", "v_photo"]
        text = f"{_('v_edit_greeting_text')}\n\n{_('v_list')}:\n" + "\n".join(_(i) for i in variables)
        result = self.bot.send_message(c.message.chat.id, text, reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(c.message.chat.id, result.id, c.from_user.id, CBT.EDIT_GREETINGS_TEXT)
        self.bot.answer_callback_query(c.id)

    def edit_greetings_text(self, m: Message):
        self.clear_state(m.chat.id, m.from_user.id, True)
        self.vertex.MAIN_CFG["Greetings"]["greetingsText"] = m.text
        logger.info(_("log_greeting_changed", m.from_user.username, m.from_user.id, m.text))
        self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")
        keyboard = K() \
            .row(B(_("gl_back"), callback_data=f"{CBT.CATEGORY}:gr"),
                 B(_("gl_edit"), callback_data=CBT.EDIT_GREETINGS_TEXT))
        self.bot.reply_to(m, _("greeting_changed"), reply_markup=keyboard)

    def act_edit_order_confirm_reply_text(self, c: CallbackQuery):
        variables = ["v_date", "v_date_text", "v_full_date_text", "v_time", "v_full_time", "v_username",
                     "v_order_id", "v_order_title", "v_photo"]
        text = f"{_('v_edit_order_confirm_text')}\n\n{_('v_list')}:\n" + "\n".join(_(i) for i in variables)
        result = self.bot.send_message(c.message.chat.id, text, reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(c.message.chat.id, result.id, c.from_user.id, CBT.EDIT_ORDER_CONFIRM_REPLY_TEXT)
        self.bot.answer_callback_query(c.id)

    def edit_order_confirm_reply_text(self, m: Message):
        self.clear_state(m.chat.id, m.from_user.id, True)
        self.vertex.MAIN_CFG["OrderConfirm"]["replyText"] = m.text
        logger.info(_("log_order_confirm_changed", m.from_user.username, m.from_user.id, m.text))
        self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")
        keyboard = K() \
            .row(B(_("gl_back"), callback_data=f"{CBT.CATEGORY}:oc"),
                 B(_("gl_edit"), callback_data=CBT.EDIT_ORDER_CONFIRM_REPLY_TEXT))
        self.bot.reply_to(m, _("order_confirm_changed"), reply_markup=keyboard)

    def act_edit_review_reply_text(self, c: CallbackQuery):
        stars = int(c.data.split(":")[1])
        variables = ["v_date", "v_date_text", "v_full_date_text", "v_time", "v_full_time", "v_username",
                     "v_order_id", "v_order_title"]
        text = f"{_('v_edit_review_reply_text', '⭐'*stars)}\n\n{_('v_list')}:\n" + "\n".join(_(i) for i in variables)
        result = self.bot.send_message(c.message.chat.id, text, reply_markup=skb.CLEAR_STATE_BTN())
        self.set_state(c.message.chat.id, result.id, c.from_user.id, CBT.EDIT_REVIEW_REPLY_TEXT, {"stars": stars})
        self.bot.answer_callback_query(c.id)

    def edit_review_reply_text(self, m: Message):
        stars = self.get_state(m.chat.id, m.from_user.id)["data"]["stars"]
        self.clear_state(m.chat.id, m.from_user.id, True)
        self.vertex.MAIN_CFG["ReviewReply"][f"star{stars}ReplyText"] = m.text
        logger.info(_("log_review_reply_changed", m.from_user.username, m.from_user.id, stars, m.text))
        self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")
        keyboard = K() \
            .row(B(_("gl_back"), callback_data=f"{CBT.CATEGORY}:rr"),
                 B(_("gl_edit"), callback_data=f"{CBT.EDIT_REVIEW_REPLY_TEXT}:{stars}"))
        self.bot.reply_to(m, _("review_reply_changed", '⭐'*stars), reply_markup=keyboard)

    def open_reply_menu(self, c: CallbackQuery):
        """
        Открывает меню ответа на сообщение (callback используется в кнопках "назад").
        """
        split = c.data.split(":")
        node_id, username, again = int(split[1]), split[2], int(split[3])
        extend = True if len(split) > 4 and int(split[4]) else False
        self.bot.edit_message_reply_markup(c.message.chat.id, c.message.id,
                                           reply_markup=kb.reply(node_id, username, bool(again), extend))

    def extend_new_message_notification(self, c: CallbackQuery):
        """
        "Расширяет" уведомление о новом сообщении.
        """
        chat_id, username = c.data.split(":")[1:]
        try:
            chat = self.vertex.account.get_chat(int(chat_id))
        except:
            self.bot.answer_callback_query(c.id)
            self.bot.send_message(c.message.chat.id, _("get_chat_error"))
            return

        text = ""
        if chat.looking_link:
            text += f"<b><i>{_('viewing')}:</i></b>\n<a href=\"{chat.looking_link}\">{chat.looking_text}</a>\n\n"

        messages = chat.messages[-10:]
        last_message_author_id = -1
        for i in messages:
            if i.author_id == last_message_author_id:
                author = ""
            elif i.author_id == self.vertex.account.id:
                author = f"<i><b>🫵 {_('you')}:</b></i> "
            elif i.author_id == 0:
                author = f"<i><b>🔵 {i.author}: </b></i>"
            elif i.author == i.chat_name:
                author = f"<i><b>👤 {i.author}: </b></i>"
            else:
                author = f"<i><b>🆘 {i.author} ({_('support')}): </b></i>"
            msg_text = f"<code>{i.text}</code>" if i.text else f"<a href=\"{i.image_link}\">{_('photo')}</a>"
            text += f"{author}{msg_text}\n\n"
            last_message_author_id = i.author_id

        self.bot.edit_message_text(text, c.message.chat.id, c.message.id,
                                   reply_markup=kb.reply(int(chat_id), username, False, False))

    # Ордер
    def ask_confirm_refund(self, call: CallbackQuery):
        """
        Просит подтвердить возврат денег.
        """
        split = call.data.split(":")
        order_id, node_id, username = split[1], int(split[2]), split[3]
        keyboard = kb.new_order(order_id, username, node_id, confirmation=True)
        self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)
        self.bot.answer_callback_query(call.id)

    def cancel_refund(self, call: CallbackQuery):
        """
        Отменяет возврат.
        """
        split = call.data.split(":")
        order_id, node_id, username = split[1], int(split[2]), split[3]
        keyboard = kb.new_order(order_id, username, node_id)
        self.bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)
        self.bot.answer_callback_query(call.id)

    def refund(self, c: CallbackQuery):
        """
        Оформляет возврат за заказ.
        """
        split = c.data.split(":")
        order_id, node_id, username = split[1], int(split[2]), split[3]
        new_msg = None
        attempts = 3
        while attempts:
            try:
                self.vertex.account.refund(order_id)
                break
            except:
                if not new_msg:
                    new_msg = self.bot.send_message(c.message.chat.id, _("refund_attempt", order_id, attempts))
                else:
                    self.bot.edit_message_text(_("refund_attempt", order_id, attempts), new_msg.chat.id, new_msg.id)
                attempts -= 1
                time.sleep(1)

        else:
            self.bot.edit_message_text(_("refund_error", order_id), new_msg.chat.id, new_msg.id)

            keyboard = kb.new_order(order_id, username, node_id)
            self.bot.edit_message_reply_markup(c.message.chat.id, c.message.id, reply_markup=keyboard)
            self.bot.answer_callback_query(c.id)
            return

        if not new_msg:
            self.bot.send_message(c.message.chat.id, _("refund_complete", order_id))
        else:
            self.bot.edit_message_text(_("refund_complete", order_id), new_msg.chat.id, new_msg.id)

        keyboard = kb.new_order(order_id, username, node_id, no_refund=True)
        self.bot.edit_message_reply_markup(c.message.chat.id, c.message.id, reply_markup=keyboard)
        self.bot.answer_callback_query(c.id)

    def open_order_menu(self, c: CallbackQuery):
        split = c.data.split(":")
        node_id, username, order_id, no_refund = int(split[1]), split[2], split[3], bool(int(split[4]))
        self.bot.edit_message_reply_markup(c.message.chat.id, c.message.id,
                                           reply_markup=kb.new_order(order_id, username, node_id, no_refund=no_refund))

    # Панель управления
    def open_cp(self, c: CallbackQuery):
        """
        Открывает основное меню настроек (редактирует сообщение).
        """
        self.bot.edit_message_text(_("desc_main"), c.message.chat.id, c.message.id,
                                   reply_markup=kb.settings_sections(self.vertex))
        self.bot.answer_callback_query(c.id)

    def open_cp2(self, c: CallbackQuery):
        """
        Открывает 2 страницу основного меню настроек (редактирует сообщение).
        """
        self.bot.edit_message_text(_("desc_main"), c.message.chat.id, c.message.id, reply_markup=skb.SETTINGS_SECTIONS_2())
        self.bot.answer_callback_query(c.id)

    def switch_param(self, c: CallbackQuery):
        """
        Переключает переключаемые настройки FPV.
        """
        split = c.data.split(":")
        section, option = split[1], split[2]
        if section == "FunPay" and option == "oldMsgGetMode":
            self.vertex.switch_msg_get_mode()
        else:
            self.vertex.MAIN_CFG[section][option] = str(int(not int(self.vertex.MAIN_CFG[section][option])))
            self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")

        sections = {
            "FunPay": kb.main_settings,
            "BlockList": kb.blacklist_settings,
            "NewMessageView": kb.new_message_view_settings,
            "Greetings": kb.greeting_settings,
            "OrderConfirm": kb.order_confirm_reply_settings,
            "ReviewReply": kb.review_reply_settings
        }
        self.bot.edit_message_reply_markup(c.message.chat.id, c.message.id,
                                           reply_markup=sections[section](self.vertex))
        logger.info(_("log_param_changed", c.from_user.username, c.from_user.id, option, section, self.vertex.MAIN_CFG[section][option]))
        self.bot.answer_callback_query(c.id)

    def switch_chat_notification(self, c: CallbackQuery):
        split = c.data.split(":")
        chat_id, notification_type = int(split[1]), split[2]

        result = self.toggle_notification(chat_id, notification_type)
        logger.info(_("log_notification_switched", c.from_user.username, c.from_user.id,
                      notification_type, c.message.chat.id, result))
        keyboard = kb.announcements_settings if notification_type in [utils.NotificationTypes.announcement,
                                                                      utils.NotificationTypes.ad] \
            else kb.notifications_settings
        self.bot.edit_message_reply_markup(c.message.chat.id, c.message.id,
                                           reply_markup=keyboard(self.vertex, c.message.chat.id))
        self.bot.answer_callback_query(c.id)

    def open_settings_section(self, c: CallbackQuery):
        """
        Открывает выбранную категорию настроек.
        """
        #
        section = c.data.split(":")[1]
        sections = {
            "main": (_("desc_gs"), kb.main_settings, [self.vertex]),
            "tg": (_("desc_ns", c.message.chat.id), kb.notifications_settings, [self.vertex, c.message.chat.id]),
            "bl": (_("desc_bl"), kb.blacklist_settings, [self.vertex]),
            "ar": (_("desc_ar"), skb.AR_SETTINGS, []),
            "ad": (_("desc_ad"), skb.AD_SETTINGS, []),
            "mv": (_("desc_mv"), kb.new_message_view_settings, [self.vertex]),
            "rr": (_("desc_or"), kb.review_reply_settings, [self.vertex]),
            "gr": (_("desc_gr", utils.escape(self.vertex.MAIN_CFG['Greetings']['greetingsText'])),
                   kb.greeting_settings, [self.vertex]),
            "oc": (_("desc_oc", utils.escape(self.vertex.MAIN_CFG['OrderConfirm']['replyText'])),
                   kb.order_confirm_reply_settings, [self.vertex])
        }

        curr = sections[section]
        self.bot.edit_message_text(curr[0], c.message.chat.id, c.message.id, reply_markup=curr[1](*curr[2]))
        self.bot.answer_callback_query(c.id)

    # Прочее
    def cancel_action(self, call: CallbackQuery):
        """
        Обнуляет состояние пользователя по кнопке "Отмена" (CBT.CLEAR_STATE).
        """
        result = self.clear_state(call.message.chat.id, call.from_user.id, True)
        if result is None:
            self.bot.answer_callback_query(call.id)

    def param_disabled(self, c: CallbackQuery):
        """
        Отправляет сообщение о том, что параметр отключен в глобальных переключателях.
        """
        self.bot.answer_callback_query(c.id, _("param_disabled"), show_alert=True)

    def send_announcements_kb(self, m: Message):
        """
        Отправляет сообщение с клавиатурой управления уведомлениями о новых объявлениях.
        """
        self.bot.send_message(m.chat.id, _("desc_an"), reply_markup=kb.announcements_settings(self.vertex, m.chat.id))

    def send_review_reply_text(self, c: CallbackQuery):
        stars = int(c.data.split(":")[1])
        text = self.vertex.MAIN_CFG["ReviewReply"][f"star{stars}ReplyText"]
        keyboard = K() \
            .row(B(_("gl_back"), callback_data=f"{CBT.CATEGORY}:rr"),
                 B(_("gl_edit"), callback_data=f"{CBT.EDIT_REVIEW_REPLY_TEXT}:{stars}"))
        if not text:
            self.bot.send_message(c.message.chat.id, _("review_reply_empty", "⭐"*stars), reply_markup=keyboard)
        else:
            self.bot.send_message(c.message.chat.id, _("review_reply_text", "⭐"*stars,
                                                       self.vertex.MAIN_CFG['ReviewReply'][f'star{stars}ReplyText']),
                                  reply_markup=keyboard)
        self.bot.answer_callback_query(c.id)

    def send_old_mode_help_text(self, c: CallbackQuery):
        self.bot.answer_callback_query(c.id)
        self.bot.send_message(c.message.chat.id, _("old_mode_help"))

    def empty_callback(self, c: CallbackQuery):
        self.bot.answer_callback_query(c.id)

    def switch_lang(self, c: CallbackQuery):
        lang = c.data.split(":")[1]
        localizer.current_language = lang
        self.vertex.MAIN_CFG["Other"]["language"] = lang
        self.vertex.save_config(self.vertex.MAIN_CFG, "configs/_main.cfg")
        if localizer.current_language == "eng":
            self.bot.answer_callback_query(c.id, "The translation may be incomplete and contain errors.\n\n"
                                                 "If you find errors in the translation, let NightStranger know.\n\n"
                                                 "Thank you :)", show_alert=True)
        self.open_cp(c)

    def open_keyboard(self, m: Message):
        self.bot.send_message(m.chat.id, "Клавиатура появилась!", reply_markup=skb.OLD_KEYBOARD)
    
    def close_keyboard(self, m: Message):
        self.bot.send_message(m.chat.id, "Клавиатура скрыта!", reply_markup=ReplyKeyboardRemove())
    
    def __register_handlers(self):
        """
        Регистрирует хэндлеры всех команд.
        """
        self.mdw_handler(self.setup_chat_notifications, update_types=['message'])
        self.msg_handler(self.reg_admin, func=lambda msg: msg.from_user.id not in self.authorized_users)
        self.cbq_handler(self.ignore_unauthorized_users, lambda c: c.from_user.id not in self.authorized_users)
        self.cbq_handler(self.param_disabled, lambda c: c.data.startswith(CBT.PARAM_DISABLED))
        self.msg_handler(self.run_file_handlers, content_types=["photo", "document"], func=lambda m: self.is_file_handler(m))

        self.msg_handler(self.send_settings_menu, commands=["menu"])
        self.cbq_handler(self.update_profile, lambda c: c.data == "update_profile")
        self.cbq_handler(self.update_adv_profile, lambda c: c.data == "update_adv_profile")
        self.msg_handler(self.send_profile, commands=["profile"])
        self.msg_handler(self.send_orders, commands=["old_orders"])
        self.msg_handler(self.change_cookie, commands=["change_cookie"])
        self.cbq_handler(self.update_profile, lambda c: c.data == CBT.UPDATE_PROFILE)
        self.msg_handler(self.act_manual_delivery_test, commands=["test_lot"])
        self.msg_handler(self.act_upload_image, commands=["upload_img"])
        self.cbq_handler(self.act_edit_greetings_text, lambda c: c.data == CBT.EDIT_GREETINGS_TEXT)
        self.msg_handler(self.edit_greetings_text,
                         func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.EDIT_GREETINGS_TEXT))
        self.cbq_handler(self.act_edit_order_confirm_reply_text, lambda c: c.data == CBT.EDIT_ORDER_CONFIRM_REPLY_TEXT)
        self.msg_handler(self.edit_order_confirm_reply_text,
                         func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.EDIT_ORDER_CONFIRM_REPLY_TEXT))
        self.cbq_handler(self.act_edit_review_reply_text, lambda c: c.data.startswith(f"{CBT.EDIT_REVIEW_REPLY_TEXT}:"))
        self.msg_handler(self.edit_review_reply_text,
                         func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.EDIT_REVIEW_REPLY_TEXT))
        self.msg_handler(self.manual_delivery_text,
                         func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.MANUAL_AD_TEST))
        self.msg_handler(self.act_ban, commands=["ban"])
        self.msg_handler(self.ban, func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.BAN))
        self.msg_handler(self.act_unban, commands=["unban"])
        self.msg_handler(self.unban, func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.UNBAN))
        self.msg_handler(self.send_ban_list, commands=["black_list"])
        self.msg_handler(self.act_edit_watermark, commands=["watermark"])
        self.msg_handler(self.edit_watermark,
                         func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.EDIT_WATERMARK))
        self.msg_handler(self.send_logs, commands=["logs"])
        self.msg_handler(self.del_logs, commands=["del_logs"])
        self.msg_handler(self.about, commands=["about"])
        self.msg_handler(self.send_system_info, commands=["sys"])
        self.msg_handler(self.restart_vertex, commands=["restart"])
        self.msg_handler(self.ask_power_off, commands=["power_off"])
        self.cbq_handler(self.send_review_reply_text, lambda c: c.data.startswith(f"{CBT.SEND_REVIEW_REPLY_TEXT}:"))

        self.msg_handler(self.send_logs, func=lambda m: m.text == "📋 Логи 📋")
        self.msg_handler(self.send_settings_menu, func=lambda m: m.text == "⚙️ Настройки ⚙️")
        self.msg_handler(self.send_system_info, func=lambda m: m.text == "📈 Система 📈")
        self.msg_handler(self.restart_vertex, func=lambda m: m.text == "🔄 Перезапуск 🔄")
        self.msg_handler(self.close_keyboard, func=lambda m: m.text == "❌ Закрыть ❌")
        self.msg_handler(self.ask_power_off, func=lambda m: m.text == "🔌 Отключение 🔌")
        self.msg_handler(self.open_keyboard, commands=["keyboard"])
        self.cbq_handler(self.act_send_funpay_message, lambda c: c.data.startswith(f"{CBT.SEND_FP_MESSAGE}:"))
        self.cbq_handler(self.open_reply_menu, lambda c: c.data.startswith(f"{CBT.BACK_TO_REPLY_KB}:"))
        self.cbq_handler(self.extend_new_message_notification, lambda c: c.data.startswith(f"{CBT.EXTEND_CHAT}:"))
        self.msg_handler(self.send_funpay_message,
                         func=lambda m: self.check_state(m.chat.id, m.from_user.id, CBT.SEND_FP_MESSAGE))
        self.cbq_handler(self.ask_confirm_refund, lambda c: c.data.startswith(f"{CBT.REQUEST_REFUND}:"))
        self.cbq_handler(self.cancel_refund, lambda c: c.data.startswith(f"{CBT.REFUND_CANCELLED}:"))
        self.cbq_handler(self.refund, lambda c: c.data.startswith(f"{CBT.REFUND_CONFIRMED}:"))
        self.cbq_handler(self.open_order_menu, lambda c: c.data.startswith(f"{CBT.BACK_TO_ORDER_KB}:"))
        self.cbq_handler(self.open_cp, lambda c: c.data == CBT.MAIN)
        self.cbq_handler(self.open_cp2, lambda c: c.data == CBT.MAIN2)
        self.cbq_handler(self.open_settings_section, lambda c: c.data.startswith(f"{CBT.CATEGORY}:"))
        self.cbq_handler(self.switch_param, lambda c: c.data.startswith(f"{CBT.SWITCH}:"))
        self.cbq_handler(self.switch_chat_notification, lambda c: c.data.startswith(f"{CBT.SWITCH_TG_NOTIFICATIONS}:"))
        self.cbq_handler(self.power_off, lambda c: c.data.startswith(f"{CBT.SHUT_DOWN}:"))
        self.cbq_handler(self.cancel_power_off, lambda c: c.data == CBT.CANCEL_SHUTTING_DOWN)
        self.cbq_handler(self.cancel_action, lambda c: c.data == CBT.CLEAR_STATE)
        self.cbq_handler(self.send_old_mode_help_text, lambda c: c.data == CBT.OLD_MOD_HELP)
        self.cbq_handler(self.empty_callback, lambda c: c.data == CBT.EMPTY)
        self.cbq_handler(self.switch_lang, lambda c: c.data.startswith(f"{CBT.LANG}:"))

    def send_notification(self, text: str | None, keyboard=None,
                          notification_type: str = utils.NotificationTypes.other, photo: bytes | None = None,
                          pin: bool = False):
        """
        Отправляет сообщение во все чаты для уведомлений из self.notification_settings.

        :param text: текст уведомления.
        :param keyboard: экземпляр клавиатуры.
        :param notification_type: тип уведомления.
        :param photo: фотография (если нужна).
        :param pin: закреплять ли сообщение.
        """
        kwargs = {}
        if keyboard is not None:
            kwargs["reply_markup"] = keyboard

        for chat_id in self.notification_settings:
            if not self.is_notification_enabled(chat_id, notification_type):
                continue

            try:
                if photo:
                    msg = self.bot.send_photo(chat_id, photo, text, **kwargs)
                else:
                    msg = self.bot.send_message(chat_id, text, **kwargs)

                if notification_type == utils.NotificationTypes.bot_start:
                    self.init_messages.append((msg.chat.id, msg.id))

                if pin:
                    self.bot.pin_chat_message(msg.chat.id, msg.id)
            except:
                logger.error(_("log_tg_notification_error", chat_id))
                logger.debug("TRACEBACK", exc_info=True)
                continue

    def add_command_to_menu(self, command: str, help_text: str) -> None:
        """
        Добавляет команду в список команд (в кнопке menu).

        :param command: текст команды.

        :param help_text: текст справки.
        """
        self.commands[command] = help_text

    def setup_commands(self):
        """
        Устанавливает меню команд.
        """
        commands = [BotCommand(f"/{i}", self.commands[i]) for i in self.commands]
        self.bot.set_my_commands(commands)

    def init(self):
        self.__register_handlers()
        logger.info(_("log_tg_initialized"))

    def run(self):
        """
        Запускает поллинг.
        """
        self.send_notification(_("bot_started"), notification_type=utils.NotificationTypes.bot_start)
        try:
            logger.info(_("log_tg_started", self.bot.user.username))
            self.bot.infinity_polling(logger_level=logging.DEBUG)
        except:
            logger.error(_("log_tg_update_error"))
            logger.debug("TRACEBACK", exc_info=True)
