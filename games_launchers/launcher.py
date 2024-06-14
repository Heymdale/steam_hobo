from games_launchers.any_game_launcher import AnyGameLaunch
from games_launchers.dont_starve_together import DontStarveTogether
from games_launchers.team_fortress_2 import TeamFortress2
from games_launchers.banana import Banana


class LaunchGame:
    @staticmethod
    def choose_game_launcher(steam_location, game_id):
        exists_game_id = {
            322330: DontStarveTogether,
            440: TeamFortress2,
            2923300: Banana,
        }

        if game_id in exists_game_id.keys():
            return exists_game_id[game_id](steam_location, game_id)
        return AnyGameLaunch(steam_location, game_id)
