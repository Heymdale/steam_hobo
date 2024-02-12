import time

import pyautogui as pag
import subprocess as sp
from steam_totp import generate_twofactor_code_for_time

from win_mgr import WinMgr


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
        self.steam_window_manager = None

    @staticmethod
    def __stop_steam():
        sp.call(['taskkill', '-IM', 'steam.exe', '/F'])
        sp.call(['taskkill', '-IM', 'steamwebhelper.exe', '/F'])

    def __start_steam(self):
        sp.Popen([self.steam_location, '-silent', '-login', self.login],
                 stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def __click_on_this_window(self):
        # To foreground window
        if self.steam_window_manager is not None:
            self.steam_window_manager.window_to_foreground()
            pag.click()

    def login_steam(self):
        # Stop all instances of steam, except steamservice.exe
        self.__stop_steam()
        time.sleep(5)
        self.__start_steam()
        # TODO: Add cycle with check if app has been appeared and exception if not in 5 minutes
        time.sleep(20)
        hwnd_steam = WinMgr.get_hwnd_by_name('Sign in to Steam')
        self.steam_window_manager = WinMgr(hwnd_steam)
        print(f'{hwnd_steam=}')
        r_left, r_top, r_right, r_bottom = self.steam_window_manager.get_window_rect_from_hwnd()
        r_height = r_bottom - r_top
        r_width = r_right - r_left
        print(f'{r_left=}, {r_top=}, {r_right=}, {r_bottom=}, {r_height=}, {r_width=}')
        if r_left > 0 and r_top > 0:
            point_on_name_field = r_left + r_width/15, r_top + r_height/3
            pag.moveTo(point_on_name_field, duration=0.5)
            self.__click_on_this_window()
            pag.typewrite(self.login)
            point_on_pass_field = r_left + r_width/15, r_top + r_height/2
            pag.moveTo(point_on_pass_field, duration=0.5)
            self.__click_on_this_window()
            pag.typewrite(self.password)
            pag.press('enter')
            # TODO: Add async request 2fa, check if steam-guard widow appear
            totp_code = generate_twofactor_code_for_time(self.totp_secret)
            print(f'{totp_code=}')
            time.sleep(15)
            point_on_totp_field = r_left + r_width/3, r_top + r_height/2
            pag.moveTo(point_on_totp_field, duration=0.5)
            self.__click_on_this_window()
            pag.typewrite(totp_code)
            pag.press('enter')
        else:
            print('Either the Steam client is already authorized or it cannot be launched.')


def test():
    ...


if __name__ == '__main__':
    test()
