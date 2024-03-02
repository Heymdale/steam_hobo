from games_launchers.game_launcher import GameLauncher


class TeamFortress2(GameLauncher):
    """Stopping with 'stop_if_none' function of GameLauncher class work badly.
    So minimum implement for close game normally.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'hl2.exe'

    def in_game_activity(self):
        ...


if __name__ == '__main__':
    ...
