#  TODO Проверка не занят ли аккаунт играми.

#  TODO Проверка не запущено ли обновление, проверять через OCR

#  TODO Пропуск пользователя по hotkey

steamexe_location = "C:\\Program Files (x86)\\Steam\\steam.exe"


class Users:
    # Write the tuple of this linux OS users, which will run steam
    # 0 index must contain name of main user, which is in sudoers, have NOPASSWD and from whom we start script
    linux_users_list = ('login1',
                        'login2',
                        )
    windows_users_list = (
        {'login': 'login1',
         'password': 'password1',
         # Shared key looks like ROdk8Ud3XjLFhVouch+fKEnBQW5=
         'shared_secret': 'shared_secret_for_steam_guard1',
         # 'games_config' is optional, all users can use common value, listed below.
         'games_config': {322330: 120, 440: 15}},
        {'login': 'login2',
         'password': 'password2',
         'shared_secret': 'shared_secret_for_steam_guard2'},
                        )


# Headline of warning window in your Linux OS
linux_warning_headline = 'Предупреждение'
# Debug True will print log in terminal
debug = True
# If loop = True, program will execute "run()" function in cycle with period "looptime_minutes".
# 24 hours = 1440 minutes
# For now there are many weak point in code, better to start with cron or windows task scheduler
loop = True
looptime_minutes = 1450
# game_time_minutes - time, which every user will run the game
# games_config:
games_config = {
    # steam_game_id : game_playtime_minutes
    322330: 120,
    440: 15,
}
game_playtime_minutes = 120
#  TODO Запуск нескольких аккаунтов одновременно
#  Count of users worked simultaneously. 0 - try to use all users.
linux_concurrent_users = 2
