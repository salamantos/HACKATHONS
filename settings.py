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
