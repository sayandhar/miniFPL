### About
FPL class contains all the methods. In addition to the parsed JSON *(obtained from FPL site)* given by ExtendedAPI, FPL extends it with additional data and sets the default values.

### Finding your Team ID & League ID

- Login to FPL website.
- Click on Points tab and check the URL.   
It'll look something like https://fantasy.premierleague.com/a/team/111/event/3. Here, 111 is your fantasy team ID *(& 3 is the gameweek)*.
- Click on the Leagues Tab and click on the required league.  
The URL will be something like https://fantasy.premierleague.com/a/leagues/standings/222/classic. Here, 222 is your league ID.

### Getting Started
First, import the FPL class.
```
from miniFPL import FPL
```
To create an FPL object, pass a team ID.
```
# lets say 111 is the team id
obj = FPL(111)

# FPL sets other argument values by itself. For example, gameweek is set to current gameweek.
# these values can also be passed explicitly
obj = FPL(111,3)
```
All FPL methods use the default values if no values are passed. However, we can pass any no. of values to these methods.
```
# this will give picks/team data for default team ID & gameweek(current)
obj.get_user_gameweek_team_picks()

# or we can check the data for a different gameweek
obj.get_user_gameweek_team_picks(gameweek=3)

# or we can pass all the values
obj.get_user_gameweek_team_picks(team_id=222,gameweek=3)
```

### Methods
