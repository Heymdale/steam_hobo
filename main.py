""" В файле sudoers должно быть прописано ALL=NOPASSWD: ALL для главного пользователя, от которого запускаем скрипт"""
import datetime
import time
import subprocess as sp
import config
import pyautogui as pag
from ewmh import EWMH
from os import environ


def logs(*args, to_warn=False):
    message = str(datetime.datetime.now())
    for s in args:
        message += str(s)
    if config.debug:
        print(message)
    if to_warn:
        # TODO: Stab, in a future version it should send the message via e-mail or telegram bot
        # Заглушка, в следующих версиях должна отправлять сообщения по почте или через телеграм бота.
        # Следует определиться на каком языке писать комментарии.
        print('\033[91m', message, '\033[0m')
    with open('./log', 'w+') as f:  # Прошлая версия была без параметра 'w+', выкидывала ошибку, пытаясь открыть
        # несуществующий файл, но эта ошибка нигде не отображалась.
        f.writelines(message)


def run(user_index, remaining_users_to_work_concurrently):
    user = config.Users.linux_users_list[user_index]
    print('Start ', user)
    #  Запускаем steam и игру
    with sp.Popen(['sudo', '-u', user, '/usr/bin/steam', '-no-browser', 'steam://rungameid/322330'],
                  stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL) as proc:
        # Непонятное поведение, после logs('Ожидание загрузки игры вышло') скрипт ничего не делает. асинхронность? баг?ы
        time.sleep(240)  # Ожидаем загрузку по таймеру
        logs('Ожидание загрузки игры вышло')
        # Закрываем предупреждение, появляющееся, если используем регистронезависимые файловые системы
        close_warning()
        dontstarve_window = activate_dontstarve_window(user)
        logs('Начинаем вводить команды')
        dontstarve_control(dontstarve_window)
        ewmh = EWMH()
        ewmh.setWmState(dontstarve_window, 1, '_NET_WM_STATE_SHADED')
        ewmh.display.flush()
        logs('Ожидание')
        if not remaining_users_to_work_concurrently == 1:
            if len(config.Users.linux_users_list) > user_index+1:
                run(user_index + 1, remaining_users_to_work_concurrently - 1)
        for i in range(config.game_time_minutes):
            # TODO Каждую минуту проверять запущена ли игра
            if True:
                time.sleep(60)
            else:
                break
        # stop_steam_game() was moved to the main function
        logs('finish run')


def stop_steam_game():
    sp.call(['sudo', 'killall', 'steam'])


def share_xserver(users):
    for user in users:
        xserver_share_command = ('xhost', '+SI:localuser:' + user)
        sp.call(xserver_share_command)


def close_warning():
    # TODO ewmh_wrapper изменен придется переписывать функцию
    ewmh = EWMH()
    ewmh_wrapper(config.warning_headline, ewmh.setCloseWindow)
    ewmh.display.flush()  # Во wrapper данная команда не работала, т.к. мы не передавали экземпляр EWMH().
    # Поэтому мы используем flush() после вызова wrapper или передаём переменную ewmh в ewmh_wrapper.


def ewmh_wrapper(substrings, ewmh_func, strong=False, case_insensitive=True):
    # С добавлением поиска строки целиком, враппер стал уже некрасив.
    # Оказалось, что приписка от какого пользователя запущена игра, не часть заголовка окна,
    # большая часть кода в данной функции написана зря.
    # TODO нужен рефакторинг, функция будет просто возвращать список окон.
    # Перед значительной переработкой сделаю коммит вместе с багом
    ewmh = EWMH()
    windows = ewmh.getClientList()
    find_windows = []
    if strong:
        if not isinstance(substrings, str):
            print('Error: You seek more than one string with strong mode')
            return
        if case_insensitive:
            find_name = substrings.lower()
        else:
            find_name = substrings
        for el in windows:
            w_name_binary = ewmh.getWmName(el)
            if w_name_binary is not None:
                if case_insensitive:
                    w_name = w_name_binary.decode('utf-8').lower()
                else:
                    w_name = w_name_binary.decode('utf-8')
                if w_name == find_name:
                    find_windows.append(el)
                    break
    else:
        find_windows = windows
        for substr in substrings:
            windows = find_windows
            find_windows = []
            if case_insensitive:
                substr = substr.lower()
            for el in windows:
                w_name_binary = ewmh.getWmName(el)
                if w_name_binary is not None:
                    if case_insensitive:
                        w_name = w_name_binary.decode('utf-8').lower()
                    else:
                        w_name = w_name_binary.decode('utf-8')
                    if -1 != w_name.find(substr):
                        find_windows.append(el)
    if len(find_windows) > 0:
        ewmh_func(find_windows[0])
        return find_windows[0]


def activate_dontstarve_window(user):
    # TODO ewmh_wrapper изменен придется переписывать функцию
    ewmh = EWMH()
    if environ.get('USER') == user:
        dontstarve_window = ewmh_wrapper("Don't Starve Together", ewmh.setActiveWindow, strong=True)
    else:
        dontstarve_window = ewmh_wrapper(("Don't Starve Together", user), ewmh.setActiveWindow)
    ewmh.display.flush()
    return dontstarve_window


def in_window_key_press(starve_window, cmd: "str pyautogui KEYBOARD_KEYS", pause_in_sec=0.5):
    ewmh = EWMH()
    ewmh.setActiveWindow(starve_window)
    ewmh.display.flush()
    pag.press(cmd)
    logs('Pressed ', cmd)
    time.sleep(pause_in_sec)


def dontstarve_control(starve_window):
    for i in range(10):
        in_window_key_press(starve_window, 'enter', 1)
    in_window_key_press(starve_window, 'left')
    in_window_key_press(starve_window, 'down')
    in_window_key_press(starve_window, 'enter')
    in_window_key_press(starve_window, 'down')
    in_window_key_press(starve_window, 'enter')
    for i in range(10):
        in_window_key_press(starve_window, 'down')
    in_window_key_press(starve_window, 'enter')


def main():
    pag.FAILSAFE = False
    users = config.Users.linux_users_list
    share_xserver(users)
    stop_steam_game()
    while True:
        start_time = datetime.datetime.now()
        start_next = start_time + datetime.timedelta(minutes=config.looptime_minutes)
        concurrent_users_count = config.concurrent_users
        concurrent_users_count == concurrent_users_count if concurrent_users_count > 0 else len(users)
        for i in range(0, len(users)):
            run(i, config.concurrent_users)
            stop_steam_game()
        if not config.loop:
            break
        end_time = datetime.datetime.now()
        diff_time_in_seconds = (start_next - end_time) // datetime.timedelta(seconds=1)
        if diff_time_in_seconds >= 0:
            time.sleep(diff_time_in_seconds)


if __name__ == '__main__':
    main()
