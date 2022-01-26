class Users:
    # Write the tuple of this linux OS users, which will run steam
    # 0 index must contain name of main user, which is in sudoers, have NOPASSWD and from whom we start script
    linux_users_list = ('heymdale',
                        'gyal',
                        'cat',
                        'viktor')


# Headline of warning window in your Linux OS
warning_headline = 'Предупреждение'
# Debug True will print log in terminal
debug = True
# If loop = True, program will execute "run()" function in cycle with period "looptime_minutes".
# 24 hours = 1440 minutes
loop = True
looptime_minutes = 1450
# game_time_minutes - time, which every user will run the game
game_time_minutes = 120
