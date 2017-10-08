# coding=utf-8

# Настраиваемые параметры бота

# Exceptions


class FatalError(Exception):
    def __init__(self, text):
        self.txt = text


class EasyError(Exception):
    def __init__(self, text):
        self.txt = text


class ContinueError(Exception):
    def __init__(self, text):
        self.txt = text


PHOTO_IS_IN_PROCESS = u'Распознаю фото...'
PHOTO_IS_NONE = u'Не похоже на штрих-код \U0001f914 \nПопробуйте сфотографировать чётче \U0001f44c'
WE_TRYING = u"Наш первый алгоритм не смог распознать фото. Поэтому мы переходим к еще 3 продвинутым. " \
            u"Они медленные... Но вы ждите \U0001f609"