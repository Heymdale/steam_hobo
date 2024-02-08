import time

import pyautogui as pag
import subprocess as sp
from steam_totp import generate_twofactor_code_for_time

import win_mgr


class LoginUserToSteam:
    """
    Class which able to log in steam win desktop app,
    it's worked only with win_mgr, which help to work with windows in OS
    """

    def __init__(self, user: dict[str], steam_location: str) -> None:
        self.login = user['login']
        self.password = user['password']
        self.totp_secret = user['shared_secret']
        # Replace directory separators as "//", "\\", "\" to "/".
        # After replace "/" to "\\"
        for sep in '//', r'\\', '\\':
            steam_location = steam_location.replace(sep, '/')
        steam_location.replace('/', r'\\')
        self.steam_location = steam_location

    @staticmethod
    def __stop_steam():
        sp.call(['taskkill', '-IM', 'steam.exe', '/F'])
        sp.call(['taskkill', '-IM', 'steamwebhelper.exe', '/F'])

    def __start_steam(self):
        sp.Popen([self.steam_location, '-silent', '-login', self.login],
                 stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def login_steam(self):
        # Stop all instances of steam, except steamservice.exe
        self.__stop_steam()
        time.sleep(5)
        self.__start_steam()
        # TODO: Add cycle with check if app has been appeared and exception if not in 5 minutes
        time.sleep(15)
        hwnd_steam = win_mgr.get_hwnd_by_name('Sign in to Steam')
        print(f'{hwnd_steam=}')
        coords = win_mgr.get_window_rect_from_name(hwnd_steam)
        print(f'{coords=}')
        if coords[0] < 0 or coords[1] < 0:
            point_on_name_field = coords[0] + 60, coords[1] + 170
            pag.moveTo(point_on_name_field, duration=0.5)
            pag.click()
            pag.typewrite(self.login)
            point_on_pass_field = coords[0] + 60, coords[1] + 260
            pag.moveTo(point_on_pass_field, duration=0.5)
            pag.click()
            pag.typewrite(self.password)
            pag.press('enter')
            # TODO: Add async request 2fa, check if steam-guard widow appear
            totp_code = generate_twofactor_code_for_time(self.totp_secret)
            print(f'{totp_code=}')
            time.sleep(2)
            point_on_totp_field = coords[0] + 300, coords[1] + 230
            pag.moveTo(point_on_totp_field, duration=0.5)
            pag.click()
            pag.typewrite(totp_code)
            pag.press('enter')
        else:
            print('Either the Steam client is already authorized or it cannot be launched.')


def test():
    ...


if __name__ == '__main__':
    test()
