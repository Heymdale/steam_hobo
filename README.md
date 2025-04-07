# steam_hobo
Now it works on windows, but maybe break on linux.
!!!WARNING!!! The games Bananas and Cats use autoclicking on their windows. To regain control, press the enter or escape button (again to enable autoclicking).

You can add another games by add script in games launchers and add import of that script in launcher.py, also in launcher.py you must add your game id in exists_game_id. After all do not forget to edit config.py.

Works on Linux with sudo command
The script just run the steam version of Don't Starve together and switches to the next user on the list every 3 hours.
It needs NOPASSWD option in sudoers file for the user we will be running the script as.
A configured in-game server is required, it will start the first server in in-game host menu.
