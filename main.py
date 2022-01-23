""" В файле sudoers должно быть прописано ALL=NOPASSWD: ALL для главного пользователя, от которого запускаем скрипт"""
import time
import subprocess as sp
import config
import pyautogui as pag
from ewmh import EWMH


def run(user):
    #  Запускаем steam и игру
    with sp.Popen(['sudo', '-u', user, '/usr/bin/steam', '-no-browser', 'steam://rungameid/322330'],
                  stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL) as proc:
        time.sleep(240)  # Ожидаем загрузки 4 минуты
        # Закрываем предупреждение
        close_warning()
        dontstarve_window = activate_dontstarve_window()
        dontstarve_control(dontstarve_window)
        ewmh = EWMH()
        ewmh.setWmState(dontstarve_window, 1, '_NET_WM_STATE_SHADED')
        ewmh.display.flush()
        time.sleep(10800)  # 3 часа
        stop_steam_game()


def stop_steam_game():
    sp.call(['sudo', 'killall', 'steam'])


def share_xserver(users):
    for user in users:
        xserver_share_command = ('xhost', '+SI:localuser:' + user)
        sp.call(xserver_share_command)


def close_warning():
    ewmh = EWMH()
    ewmh_wrapper(config.warning_headline, ewmh.setCloseWindow)
    ewmh.display.flush()  # Во wrapper данная команда не работала, т.к. мы не передавали экземпляр EWMH().
    # Поэтому мы используем flush() после вызова wrapper или передаём переменную ewmh в ewmh_wrapper.


def ewmh_wrapper(name, ewmh_func):
    ewmh = EWMH()
    windows = ewmh.getClientList()
    find_windows = []
    for el in windows:
        w_name = ewmh.getWmName(el)
        if w_name is not None:
            if -1 != w_name.decode('utf-8').find(name):
                find_windows.append(el)
                break
    if len(find_windows) > 0:
        ewmh_func(find_windows[0])  # В данной версии запускаем по одному экземпляру, коллизии не обрабатываем
        return find_windows[0]


def activate_dontstarve_window():
    ewmh = EWMH()
    dontstarve_window = ewmh_wrapper("Don't Starve Together", ewmh.setActiveWindow)
    return dontstarve_window


def in_window_key_press(starve_window, cmd: "str pyautogui KEYBOARD_KEYS", pause_in_sec=0.5):
    ewmh = EWMH()
    ewmh.setActiveWindow(starve_window)
    pag.press(cmd)
    time.sleep(pause_in_sec)


def dontstarve_control(starve_window):
    for i in range(5):
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
    for user in users:
        run(user)


if __name__ == '__main__':
    main()
