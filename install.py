import os

try:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('logs/logs.txt'):
        log_file = open('logs/logs.txt', 'a')
        reset_file = open('logs/reset_file.txt', 'a')

    secret_settings = open('secret_settings.py', 'a')
except Exception as e:
    print('Exception on creating directories' + e.message)


