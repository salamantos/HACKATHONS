# coding=utf-8

import re
from Queue import Queue

from settings import *
from secret_settings import BOT_TOKEN
from Telegram_requests import *
import threading
import json
import requests
from image_recognition import get_info_by_url

# Включение бота
reset_messages = raw_input('Reset messages? y/n\n')
if reset_messages == 'y':
    reset_messages = True
else:
    reset_messages = False

try:
    log_file = open('logs/logs.txt', 'a')
except Exception, err_exception:
    sys.stderr.write('error: {}'.format(err_exception))
    exit(1)
log_write(log_file, 'sys', '------------- Начало сеанса -------------')
bot = init_bot(BOT_TOKEN)
try:
    write_bot_name(log_file, bot)
    log_write(log_file, 'sys', 'Successfully started')
except FatalError as exc_txt:
    log_write(log_file, 'sys', exc_txt.txt)
    exit(1)
offset = 0

# Пропускаем пропущенные сообщения
if reset_messages:
    updates = get_updates_for_bot(bot, offset)
    if updates:
        try:
            with open('logs/reset_file.txt', 'a') as reset_file:
                reset_file.write(str(updates))
        except Exception, err_exception:
            sys.stderr.write('error: {}'.format(err_exception))
            exit(1)

        offset = updates[-1].update_id + 1

log_write(log_file, 'sys', 'Successfully skipped messages')

print "bot started\n"  # Используется, чтобы из консоли можно было понять, что старт прошел успешно


def get_photo_url(photo):
    first_req = 'https://api.telegram.org/bot' + BOT_TOKEN + '/getFile?file_id=' + photo.file_id
    # print first_req
    res_req = requests.get(first_req).content
    x = json.loads(res_req)
    return 'https://api.telegram.org/file/bot' + BOT_TOKEN + '/' + x['result']['file_path']


def multi_thread_user_communication(user_id):
    print user_id
    try:
        personal_update = threads[user_id].get()

        # Получаем информацию о сообщении
        offset, user_id, chat_id, username, text, message_date, photo = extract_update_info(personal_update)
        print personal_update

        if photo is not None:
            result = bot.send_message(chat_id, PHOTO_IS_IN_PROCESS).wait()
            print result
            da = get_info_by_url(bot, chat_id, user_id, get_photo_url(photo))
        else:
            answer(log_file, bot, user_id, chat_id, PHOTO_IS_NONE, reply_markup, del_msg=False)
            return
        k = 0
        for i in da:
            if k == 0:
                print i
                if i is not None:
                    answer(log_file, bot, user_id, chat_id, i, reply_markup, del_msg=False)
                else:
                    answer(log_file, bot, user_id, chat_id, "Мы не знаем что это :(", reply_markup, del_msg=False)
            elif k == 1:
                print i
                if i is not None:
                    answer(log_file, bot, user_id, chat_id, "Средняя оценка \n" + i, reply_markup, del_msg=False)
                else:
                    answer(log_file, bot, user_id, chat_id, "Данных о средней оценке нет :(", reply_markup, del_msg=False)
            else:
                print i
                if i is not None:
                    answer(log_file, bot, user_id, chat_id, "Всего отзывов\n" + i, reply_markup, del_msg=False)
                else:
                    answer(log_file, bot, user_id, chat_id, "Отзовов нет :( ", reply_markup, del_msg=False)
            k+=1

    except ContinueError as exc_txt:
        answer(log_file, bot, user_id, chat_id, exc_txt.txt,
               reply_markup, del_msg=False)
    except EasyError as exc_txt:
        log_write(log_file, 'sys', exc_txt.txt)


threads = dict()
# Запуск прослушки Телеграма
try:
    answer_text = u'<Заготовка под ответ>'
    reply_markup = None  # Клавиатура
    while True:
        try:  # Отлавиваем только EasyError, остальное завершает работу
            updates = get_updates_for_bot(bot, offset)  # Если нет обновлений, вернет пустой список
            for update in updates:
                # Получаем информацию о сообщении
                offset, user_id, _, _, _, _, _ = extract_update_info(update)

                if user_id not in threads:
                    threads[user_id] = Queue()
                threads[user_id].put(update)

                t = threading.Thread(target=multi_thread_user_communication, args=[user_id])
                t.start()

                offset += 1  # id следующего обновления

            time.sleep(1)
        except Exception as e:
            offset += 1  # id следующего обновления
            print e.message

except KeyboardInterrupt:
    log_write(log_file, 'endl', '')
    log_write(log_file, 'sys', 'Бот остановлен.')
except FatalError as exc_txt:
    log_write(log_file, 'sys', exc_txt.txt)
except Exception, exc_txt:
    log_write(log_file, 'sys', 'Неизвестная ошибка: {}'.format(exc_txt), sys_time())
finally:
    log_write(log_file, 'sys', '------------- Конец сеанса --------------\n\n\n')
    log_file.close()
    # storage.close_db()
