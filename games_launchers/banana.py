import time
from random import randint

import pyautogui as pag

from games_launchers.game_launcher import GameLauncher
from win_mgr import WinMgr


class Banana(GameLauncher):
    """Don't forget to add this class and game id to launcher.py"""
    _process_names = 'banana.exe'
    _window_title = 'Banana'
    _window = None

    def in_window_click_center(self, point, pause_in_sec=0):
        if self._window is None:
            return
        # We must restore window if it minimized.
        # We must foreground window if it in background.
        # We will not check, we will do.
        self._window.restore_window()
        self._window.window_to_foreground()
        pag.moveTo(point[0] + randint(0, 30),
                   point[1] + randint(0, 30))
        pag.click()
        time.sleep(pause_in_sec)

    def in_game_activity(self):
        # Wait until game start
        game_hwnd = self.wait_hwnd()
        if not game_hwnd:
            return
        self._window = WinMgr(game_hwnd)
        print(f'{game_hwnd=}')
        r_left, r_top, r_right, r_bottom = self._window.get_window_rect_from_hwnd()
        print(f'{r_left=}, {r_top=}, {r_right=}, {r_bottom=}')
        point_around_center = (r_left + r_right)/2, (r_top + r_bottom)/2
        for _ in range(500+randint(0, 500)):
            self.in_window_click_center(point_around_center)


if __name__ == '__main__':
    ...
