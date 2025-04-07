import time
from random import randint
from typing import Union, Optional, Tuple
import threading

import pyautogui as pag
import pynput

from games_launchers.game_launcher import GameLauncher
from win_mgr import WinMgr


class Banana(GameLauncher):
    """Don't forget to add this class and game id to launcher.py"""
    _process_names = 'banana.exe'
    _window_title = 'Banana'
    _window = None
    _is_to_click = True

    @staticmethod
    def click():
        mouse = pynput.mouse.Controller()
        mouse.press(pynput.mouse.Button.left)
        time.sleep(0.03)
        mouse.release(pynput.mouse.Button.left)

    def set_window(self):
        # Wait until game start
        game_hwnd = self.wait_hwnd()
        if not game_hwnd:
            return None
        self._window = WinMgr(game_hwnd)
        print(f'{game_hwnd=}')

    def get_click_point(self) -> None | Tuple[float, int]:
        r_left, r_top, r_right, r_bottom = self._window.get_window_rect_from_hwnd()
        x, y = (r_left + r_right) / 2, (r_top + r_bottom) / 2
        return x + randint(0, 15), y + randint(0, 15)

    # Real parameters will pass in threading.Thread
    def in_window_click(self,
                        listener: Optional[pynput.keyboard.Listener] = None,
                        clicks_interval_in_secs: Union[float, int] = 0.1,
                        min_click_count: int = 100,
                        plus_random_click_count: int = 0
                        ):

        self.set_window()
        if self._window is None:
            pynput.keyboard.Listener.stop(listener)
            return
        for _ in range(min_click_count + randint(0, plus_random_click_count)):
            if not self._is_to_click:
                time.sleep(clicks_interval_in_secs)
                continue
            # We must restore window if it minimized.
            # We must foreground window if it in background.
            # We will not check, we will do.
            self._window.restore_window()
            self._window.window_to_foreground()
            pag.moveTo(self.get_click_point())
            self.click()
            time.sleep(clicks_interval_in_secs)
        pynput.keyboard.Listener.stop(listener)

    def on_press(self, key):
        if key == pynput.keyboard.Key.esc or key == pynput.keyboard.Key.enter:
            print('Change the flag')
            self._is_to_click = not self._is_to_click
        else:
            print('Not rule key')

    def in_game_activity(self,
                         clicks_interval_in_secs=0.0666,
                         min_click_count=500,
                         plus_random_click_count=700,
                         ):

        listener = pynput.keyboard.Listener(on_press=self.on_press)
        listener.start()
        threading.Thread(target=self.in_window_click,
                         kwargs={'listener': listener,
                                 'clicks_interval_in_secs': clicks_interval_in_secs,
                                 'min_click_count': min_click_count,
                                 'plus_random_click_count': plus_random_click_count},
                         daemon=False).start()
        # With join() main algorithm will wait until listener thread are exit, else it will run further.
        listener.join()


if __name__ == '__main__':
    ...
