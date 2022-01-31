#  TODO Проверка не занят ли аккаунт играми.

#  TODO Проверка не запущено ли обновление, проверять через OCR,
#  минимум два языка

#  TODO Пропуск пользователя по hotkey

#  TODO TO RELEASE вход в аккаунт, связь с SDA, расширение списка игр,
#  отдельные скрипты под игры, подключение их через данный config.py
#  или доп конфиг файл.


class Users:
    # Write the tuple of this linux OS users, which will run steam
    # 0 index must contain name of main user, which is in sudoers, have NOPASSWD and from whom we start script
    linux_users_list = ('cat',
                        'viktor',
                        'heymdale',
                        'gyal',
                        )


# Headline of warning window in your Linux OS
warning_headline = 'Предупреждение'
# Debug True will print log in terminal
debug = True
# If loop = True, program will execute "run()" function in cycle with period "looptime_minutes".
# 24 hours = 1440 minutes
loop = True
looptime_minutes = 1450
# game_time_minutes - time, which every user will run the game
game_time_minutes = 120
#  TODO Запуск нескольких аккаунтов одновременно
#  Count of users worked simultaneously. 0 - try to use all users.
concurrent_users = 2
