from games_launchers.game_launcher import GameLauncher


class ButtSlapper(GameLauncher):
    """Stopping with 'stop_if_none' function of GameLauncher class work badly.
    So minimum implement for close game normally.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'Amarillo\'s Butt Slapper.exe'

    def in_game_activity(self):
        ...


if __name__ == '__main__':
    ...
