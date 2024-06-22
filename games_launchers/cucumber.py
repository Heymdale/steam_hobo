from games_launchers.banana import Banana


class Cucumber(Banana):
    """Just inherit from banana, then we code in_app_behavior, this class will copy it.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'Banana and Cucumber.exe'
    _window_title = 'Banana and Cucumber'
    _window = None


if __name__ == '__main__':
    ...
