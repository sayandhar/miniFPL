BASE_URL = 'https://fantasy.premierleague.com/drf/'

FPL_DATA = BASE_URL + 'bootstrap-static'

# (player id)
PLAYER_DATA = BASE_URL + 'element-summary/{}'
# (gameweek)
DREAM_TEAM_DATA = BASE_URL + 'dream-team/{}'
# (team id)
USER_DATA = BASE_URL + 'entry/{}'
# (gameweek)
USER_GAMEWEEK_TEAM_DATA = USER_DATA + '/event/{}/picks'
