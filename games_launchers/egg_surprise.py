from games_launchers.banana import Banana


class EggSurprise(Banana):
    """Just inherit from banana, then we code in_app_behavior, this class will copy it.
    Don't forget to add this class and game id to launcher.py"""
    _process_names = 'Egg Surprise.exe'
    _window_title = 'Egg Surprise'
    _window = None

    def in_game_activity(self,
                         clicks_interval_in_secs=0.0666,
                         min_click_count=2000,
                         plus_random_click_count=700,
                         ):
        super().in_game_activity(
            clicks_interval_in_secs=clicks_interval_in_secs,
            min_click_count=min_click_count,
            plus_random_click_count=plus_random_click_count)


if __name__ == '__main__':
    ...
