from games_launchers.banana import Banana


class EggSurprise(Banana):
    """Just inherit from banana, then we code in_app_behavior, this class will copy it.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'Egg Surprise.exe'
    _window_title = 'Egg Surprise'
    _window = None


if __name__ == '__main__':
    ...
