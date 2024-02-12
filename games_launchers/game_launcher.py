import time
from abc import ABC, abstractmethod
import subprocess as sp

import pyautogui as pag


class GameLauncher(ABC):

    _process_names = None

    def __init__(self, steam_location, steam_game_id):
        # Replace directory separators as "//", "\\", "\" to "/".
        # After replace "/" to "\\"
        # Should I or how to "DRY" it with same code in login_steam.py
        for sep in '//', r'\\', '\\':
            steam_location = steam_location.replace(sep, '/')
        steam_location.replace('/', r'\\')
        self.steam_location = steam_location
        self.steam_game_id = steam_game_id
        # For test purposes
        print(f'The game with {steam_game_id} id is initials')

    def run(self):
        sp.Popen([self.steam_location, f'steam://rungameid/{self.steam_game_id}'],
                 stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    @abstractmethod
    def in_game_activity(self):
        ...

    @staticmethod
    def _start_if_steam_cloud_problem():
        """
        As example, DST program shutout without saving, this call problem with cloud saves on next start.
        As a stab I will call 'enter' press to start anyway.
        It will 3 times with interval to wait until window about problem appear
        and to minimize risk of other window sets to foreground.
        """
        for i in range(3):
            time.sleep(1)
            pag.press('enter')

    def _stop_if_none(self):
        # We can't know which process is a game,
        # so we stop steam, it must close game.
        sp.call(['taskkill', '-IM', 'steam.exe', '/F'])
        sp.call(['taskkill', '-IM', 'steamwebhelper.exe', '/F'])
        # We already authorized in steam,
        # and it must start without "sign in" window
        sp.Popen([self.steam_location, '-silent'],
                 stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        time.sleep(60)

    def stop(self):
        if self._process_names is not None:
            for proc_name in self._process_names:
                sp.call(['taskkill', '-IM', proc_name, '/F'])
                time.sleep(60)
            return
        self._stop_if_none()


if __name__ == 'main':
    ...
