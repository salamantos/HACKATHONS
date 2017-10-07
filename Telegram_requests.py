# coding=utf-8
import settings
from settings import FatalError, EasyError
from logs import *
from twx.botapi import TelegramBot, Error

reload(sys)
sys.setdefaultencoding('utf8')


# Модуль запросов к Телеграму
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Получаем данные из обновления
def extract_update_info(update_object):
    try:
        if update_object.edited_message is not None:
            raise EasyError('extract_update_info error: message')
        elif update_object.message is None:
            raise EasyError('extract_update_info error: None message')
        elif update_object.message.new_chat_member is not None \
                or update_object.message.left_chat_member is not None:
            raise EasyError('extract_update_info error: User join/left')
    except AttributeError:
        raise EasyError('extract_update_info error: AttributeError')

    # try AttributeError
    update_id = update_object.update_id
    received_user_id = update_object.message.sender.id
    received_username = update_object.message.sender.username
    chat_id = update_object.message.chat.id
    # chat_type = update_object.message.chat.type  # Пока работаем с приватным, проверить
    request_date = update_object.message.date
    received_text = update_object.message.text
    photo = None
    if update_object.message.photo is not None:
        photo = update_object.message.photo[-1]

    return update_id, received_user_id, chat_id, received_username, received_text, request_date, photo


# Пытаемся отправить сообщение из очереди
def send_answer_from_queue(log_file, bot, send_user_id, chat_id, send_answer_text,
                           reply_markup):
    if reply_markup is None:
        result = bot.send_message(chat_id, send_answer_text).wait()
        # print 1
        log_write(log_file, 'bot', result)
    else:
        result = bot.send_message(chat_id, send_answer_text, reply_markup=reply_markup).wait()
        # print 2
        log_write(log_file, 'bot', result)

    if isinstance(result, Error):
        print "Error while sending: "
        print result
        return False

    return True


# Отвечает за отправку и временное хранение сообщений
def answer(log_file, bot, send_user_id, chat_id, send_answer_text, reply_markup=None, del_msg=False):
    send_answer_from_queue(log_file, bot, send_user_id,
                           chat_id, send_answer_text,
                           reply_markup)


# Инициализация бота
def init_bot(init_token):
    bot = TelegramBot(init_token)
    bot.update_bot_info().wait()
    return bot


# Вывод в логи имени бота
def write_bot_name(log_file, bot):
    try:
        log_write(log_file, 'sys', '{}\n'.format(bot.username))
    except TypeError:
        raise FatalError('No internet connection')


# Получение обновлений с сервера Телеграма
def get_updates_for_bot(bot, offset):
    result = bot.get_updates(offset).wait()
    if result is None:
        result = []
    return result
