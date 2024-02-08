import time

import pyautogui as pag

from games_launchers.game_launcher import GameLauncher


class DontStarveTogether(GameLauncher):

    __process_names = ('dontstarve_steam.exe', 'dontstarve_steam_x64.exe')

    @staticmethod
    def in_window_key_press(cmd: "str pyautogui KEYBOARD_KEYS", pause_in_sec=0.5):
        pag.press(cmd)
        time.sleep(pause_in_sec)

    def in_game_activity(self):
        # Wait until game start
        time.sleep(60*3)
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


if __name__ == '__main__':
    ...
