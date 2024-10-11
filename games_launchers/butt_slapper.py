from typing import Tuple
import time

import pyautogui as pag

from games_launchers.game_launcher import GameLauncher
from win_mgr import WinMgr


class ButtSlapper(GameLauncher):
    """In game this script should click the start button,
    the coordinates are calculated relative to the window size"""
    _process_names = 'Amarillo\'s Butt Slapper.exe'
    _window_title = 'Amarillo\'s Butt Slapper'
    _window = None

    def calc_target_position(self) -> Tuple[int, int]:
        r_left, r_top, r_right, r_bottom = self._window.get_window_rect_from_hwnd()
        # Don't try to check if app in fullscreen mode,
        # always take into account the height of the heading, which is 40 px.
        r_top = r_top + 40
        target_x = (r_left + r_right) // 2
        vertical_ratio = 0.66 - 5.6/(r_bottom - r_top)
        target_y = int(r_top + vertical_ratio * (r_bottom - r_top))
        return target_x, target_y

    def click_start_button(self):
        if self._window is None:
            return
        # We must restore window if it minimized.
        # We must foreground window if it in background.
        # We will not check, we will do.
        self._window.restore_window()
        self._window.window_to_foreground()
        point = self.calc_target_position()
        pag.moveTo(point)
        pag.click()

    def move_to_target_position(self):
        self._window.restore_window()
        self._window.window_to_foreground()
        point = self.calc_target_position()
        pag.moveTo(point)

    def in_game_activity(self):
        game_hwnd = self.wait_hwnd()
        if not game_hwnd:
            return
        self._window = WinMgr(game_hwnd)
        time.sleep(15)
        print(f'{game_hwnd=}')
        self.click_start_button()


if __name__ == '__main__':
    ...
