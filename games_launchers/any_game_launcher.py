from games_launchers.game_launcher import GameLauncher


class AnyGameLaunch(GameLauncher):
    def in_game_activity(self):
        self._start_if_steam_cloud_problem()
