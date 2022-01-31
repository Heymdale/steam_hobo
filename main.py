""" В файле sudoers должно быть прописано ALL=NOPASSWD: ALL для главного пользователя, от которого запускаем скрипт"""
import datetime
import time
import subprocess as sp
import config
import pyautogui as pag
from ewmh import EWMH


def logs(*args, to_warn=False):
    message = str(datetime.datetime.now()) + ' '
    for s in args:
        message += str(s)
    if config.debug:
        print(message)
    if to_warn:
        # TODO: Stab, in a future version it should send the message via e-mail or telegram bot
        # Заглушка, в следующих версиях должна отправлять сообщения по почте или через телеграм бота.
        # Следует определиться на каком языке писать комментарии.
        print('\033[91m', message, '\033[0m')
    with open('./log', 'a') as f:  # Прошлая версия была без параметра 'w+', выкидывала ошибку, пытаясь открыть
        # несуществующий файл, но эта ошибка нигде не отображалась.
        f.writelines(message)

def find_window_of_user(current_game_windows, dontstarve_windows, concurrent_users_count):
    for el in dontstarve_windows:
        for i in range(concurrent_users_count):
            if not el == current_game_windows[i]:
                dontstarve_window = el
                current_game_windows[i] = el
                return dontstarve_window


def run(user_index, concurrent_users_count, current_game_windows):
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
        dontstarve_windows = ewmh_wrapper("Don't Starve Together", strong=True)
        dontstarve_window = find_window_of_user(current_game_windows, dontstarve_windows, concurrent_users_count)
        logs('Начинаем вводить команды')
        dontstarve_control(dontstarve_window)
        ewmh = EWMH()
        ewmh.setWmState(dontstarve_window, 1, '_NET_WM_STATE_SHADED')
        ewmh.display.flush()
        logs('"Играем" отведенное время')


def stop_steam_game():
    sp.call(['sudo', 'killall', 'steam'])


def share_xserver(users):
    for user in users:
        xserver_share_command = ('xhost', '+SI:localuser:' + user)
        sp.call(xserver_share_command)


def close_warning():
    ewmh = EWMH()
    warning_windows = ewmh_wrapper(config.warning_headline)
    for el in warning_windows:
        ewmh.setCloseWindow(el)
    ewmh.display.flush()


def ewmh_wrapper(substrings, strong=True, case_insensitive=False):
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
    return find_windows


def activate_dontstarve_window(window):
    ewmh = EWMH()
    ewmh.setActiveWindow(window)
    ewmh.display.flush()
    time.sleep(0.1) # TODO провести тесты, нужна ли задержка и достаточна ли она для фокуса на нужном окне


def in_window_key_press(starve_window, cmd: "str pyautogui KEYBOARD_KEYS", pause_in_sec=0.2):
    activate_dontstarve_window(starve_window)
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
        i = 0
        while i < len(users):
            current_game_windows = [None] * concurrent_users_count
            for concurrent in range(i, i + concurrent_users_count):
                if i < len(users):
                    run(i, concurrent_users_count, current_game_windows)
            i += concurrent_users_count
            for i in range(config.game_time_minutes):
                # TODO Каждую минуту проверять запущена ли игра
                if True:
                    time.sleep(60)
                else:
                    break
            stop_steam_game()
            logs('finish run')
        if not config.loop:
            break
        end_time = datetime.datetime.now()
        diff_time_in_seconds = (start_next - end_time) // datetime.timedelta(seconds=1)
        if diff_time_in_seconds >= 0:
            time.sleep(diff_time_in_seconds)


if __name__ == '__main__':
    main()
