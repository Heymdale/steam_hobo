import datetime
import time
import config
import pyautogui as pag

import login_steam_desktop.login_steam as ls
from games_launchers.launcher import LaunchGame


def logs(*args, to_warn=False):
    message = str(datetime.datetime.now()) + ' '
    for s in args:
        message += str(s)
    if config.debug:
        print(message)
    if to_warn:
        # TODO: Stab, in a future version it should send the message via e-mail or telegram bot
        print('\033[91m', message, '\033[0m')
    with open('./log', 'a', encoding="utf-8") as f:
        f.writelines(message)


def run_steam(user_index, steam_location):
    user = config.Users.windows_users_list[user_index]
    print('Start ', user['login'])
    steam_foo = ls.LoginUserToSteam(user, steam_location)
    steam_foo.login_steam()


def main_os():
    pag.FAILSAFE = False
    users = config.Users.windows_users_list
    steam_location = config.steamexe_location
    while True:
        start_time = datetime.datetime.now()
        start_next = start_time + datetime.timedelta(minutes=config.looptime_minutes)
        i = 0
        while i < len(users):
            user = users[i]
            logs('Начало обхода, i=', i)
            run_steam(i, steam_location)
            games_config = config.games_config
            if 'games_config' in user.keys():
                games_config = user['games_config']
            for game_id in games_config.keys():
                playtime = int(games_config[game_id])
                game = LaunchGame.choose_game_launcher(steam_location, game_id)
                game.run()
                game.in_game_activity()
                for j in range(playtime):
                    # TODO Каждую минуту проверять запущена ли игра
                    if True:
                        time.sleep(60)
                    else:
                        break
                game.stop()

            logs('finish run')
            i += 1
            logs('Конец обхода, i=', i,)
            time.sleep(60)
        if not config.loop:
            break
        end_time = datetime.datetime.now()
        diff_time_in_seconds = (start_next - end_time) // datetime.timedelta(seconds=1)
        if diff_time_in_seconds >= 0:
            logs('Ждем ', diff_time_in_seconds, ' секунд')
            time.sleep(diff_time_in_seconds)


if __name__ == '__main__':
    main_os()
