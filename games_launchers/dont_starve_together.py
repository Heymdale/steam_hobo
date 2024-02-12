import time

import pyautogui as pag

from games_launchers.game_launcher import GameLauncher
from win_mgr import WinMgr


class DontStarveTogether(GameLauncher):

    _process_names = ('dontstarve_steam.exe', 'dontstarve_steam_x64.exe')
    __window_title = 'Don\'t Starve Together'
    __window = None

    def in_window_key_press(self, cmd: "str pyautogui KEYBOARD_KEYS", pause_in_sec=0.5):
        if self.__window is None:
            return
        # We must restore window if it minimized.
        # We must foreground window if it in background.
        # We will not check, we will do.
        # If cursor point on dst menu, up/down commands will list chosen item from the point,
        # so we must move cursor out for example to 0,0.
        pag.moveTo(0, 0)
        self.__window.restore_window()
        self.__window.window_to_foreground()
        pag.press(cmd)
        print(f'Pressed key {cmd}')
        time.sleep(pause_in_sec)

    def in_game_activity(self):
        self._start_if_steam_cloud_problem()
        # Wait until game start
        time.sleep(60*2)
        dst_hwnd = WinMgr.get_hwnd_by_name(self.__window_title)
        self.__window = WinMgr(dst_hwnd)
        for i in range(10):
            self.in_window_key_press('enter', 1)
        self.in_window_key_press('left')
        self.in_window_key_press('down')
        self.in_window_key_press('enter')
        self.in_window_key_press('down')
        self.in_window_key_press('enter')
        for i in range(10):
            self.in_window_key_press('down')
        self.in_window_key_press('enter')
        # To minimize resources consumption need minimize window
        self.__window.minimize_window()


if __name__ == '__main__':
    ...
