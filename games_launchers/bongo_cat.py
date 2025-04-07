from games_launchers.banana import Banana


class BongoCat(Banana):
    """Just inherit from banana, then we code in_app_behavior, this class will copy it.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'BongoCat.exe'
    _window_title = 'BongoCat'
    _window = None


if __name__ == '__main__':
    ...
