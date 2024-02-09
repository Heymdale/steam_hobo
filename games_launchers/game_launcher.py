from abc import ABC, abstractmethod
import subprocess as sp


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

    def _stop_if_none(self):
        # We can't know which process is a game,
        # so we stop steam, it must close game.
        sp.call(['taskkill', '-IM', 'steam.exe', '/F'])
        sp.call(['taskkill', '-IM', 'steamwebhelper.exe', '/F'])
        # We already authorized in steam,
        # and it must start without "sign in" window
        sp.Popen([self.steam_location, '-silent'],
                 stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def stop(self):
        if self._process_names is not None:
            for proc_name in self._process_names:
                sp.call(['taskkill', '-IM', proc_name, '/F'])
            return
        self._stop_if_none()


if __name__ == 'main':
    ...
