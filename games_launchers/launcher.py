from games_launchers.any_game_launcher import AnyGameLaunch
from games_launchers.dont_starve_together import DontStarveTogether
from games_launchers.team_fortress_2 import TeamFortress2
from games_launchers.banana import Banana
from games_launchers.bongo_cat import BongoCat
from games_launchers.cats import Cats
from games_launchers.egg import Egg
from games_launchers.cucumber import Cucumber
from games_launchers.egg_surprise import EggSurprise
from games_launchers.butt_slapper import ButtSlapper


class LaunchGame:
    @staticmethod
    def choose_game_launcher(steam_location, game_id):
        exists_game_id = {
            322330: DontStarveTogether,
            440: TeamFortress2,
            2923300: Banana,
            2977660: Cats,
            2784840: Egg,
            3015610: Cucumber,
            3017120: EggSurprise,
            3231090: ButtSlapper,
            3419430: BongoCat
        }

        if game_id in exists_game_id.keys():
            return exists_game_id[game_id](steam_location, game_id)
        return AnyGameLaunch(steam_location, game_id)
