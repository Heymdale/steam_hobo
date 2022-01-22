""" В файле sudoers должно быть прописано ALL=NOPASSWD: ALL для главного пользователя, от которого запускаем скрипт"""
import time
import subprocess as sp
import config
import pyautogui as pag
from ewmh import EWMH


def run(user):
    # Запускаем стим без браузера
    with sp.Popen(['sudo', '-u', user, '/usr/bin/steam', '-no-browser&'],
                  stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL) as proc:
        pass
    time.sleep(240)  # Ожидаем загрузки 4 минуты
    #  Запускаем игру
    with sp.Popen(['sudo', '-u', user, '/usr/bin/steam', 'steam://rungameid/322330'],
                  stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL) as proc:
        pass


def stop_steam_game():
    sp.call(['sudo', 'killall', 'steam'])


def share_xserver(users):
    for user in users:
        xserver_share_command = ('xhost', '+SI:localuser:' + user)
        sp.call(xserver_share_command)


def activate_dontstarve_window():
    time.sleep(240) #   Ожидаем загрузки 4 минуты
    ewmh = EWMH()
    windows = ewmh.getClientList()
    starve_find_name = 'starve'
    starve_windows = []
    for el in windows:
        if ewmh.getWmName(el).decode('utf-8').lower().find(starve_find_name) != -1:
            starve_windows.append(el)
    ewmh.setActiveWindow(starve_windows[0])  # В данной версии программы не используем параллельно запущенные копии игры
    ewmh.display.flush()

def dontstarve_control():
    for i in range(20):
        pag.press('enter')
        time.sleep(2)
    pag.press('down')
    pag.press('down')
    pag.press('enter')
    pag.press('enter')
    for i in range(10):
        pag.press('down')
    pag.press('enter')


def main():
    pag.FAILSAFE = False
    users = config.Users.linux_users_list
    share_xserver(users)
    for user in users:
        stop_steam_game()
        run(user)
        activate_dontstarve_window()
        dontstarve_control()
        time.sleep(10800)   # 3 часа


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
