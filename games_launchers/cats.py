from games_launchers.banana import Banana


class Cats(Banana):
    """Just inherence from banana, then we code in_app_behavior, this class will copy it.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'cats.exe'


if __name__ == '__main__':
    ...
