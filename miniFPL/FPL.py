import requests
from operator import itemgetter
from . import links



class CoreAPI:
    """
    Getters for json data directly from official FPL links
    """

    def __init__(self):
        pass


    def get_fpl_data(self):
        try:
            fpl_data = requests.get(links.FPL_DATA).json()
        except requests.exceptions.SSLError:
            fpl_data = requests.get(links.FPL_DATA,verify=False).json()
        return fpl_data


    def get_player_data(self,player_id):
        try:
            player_data = requests.get(links.PLAYER_DATA.format(player_id)).json()
        except requests.exceptions.SSLError:
            player_data = requests.get(links.PLAYER_DATA.format(player_id),verify=False).json()
        return player_data


    def get_dream_team_data(self,gameweek):
        try:
            dream_team_data = requests.get(links.PLAYER_DATA.format(gameweek)).json()
        except requests.exceptions.SSLError:
            dream_team_data = requests.get(links.PLAYER_DATA.format(gameweek),verify=False).json()
        return dream_team_data


    def get_user_gameweek_picks_data(self,team_id,gameweek):
        try:
            user_gameweek_picks_data = requests.get(links.USER_GAMEWEEK_PICKS_DATA.format(team_id,gameweek)).json()
        except requests.exceptions.SSLError:
            user_gameweek_picks_data = requests.get(links.USER_GAMEWEEK_PICKS_DATA.format(team_id,gameweek),verify=False).json()
        return user_gameweek_picks_data


    def get_user_data(self,team_id):
        try:
            user_data = requests.get(links.USER_DATA.format(team_id)).json()
        except requests.exceptions.SSLError:
            user_data = requests.get(links.USER_DATA.format(team_id),verify=False).json()
        return user_data



class FPL:

    """
    Importable FPL class containing all user accessible methods
    Each instance is bound to a team_id at init

    Methods:
    ========
    get_entry_data(gameweek):
    -------------------------
    Param:
        gameweek - default current week else given week

    Description:
        mohawk

    get_picks_data(gameweek):
    -------------------------
    Param:
        gameweek - default current week else given week
    
    Description:
        Get detailed fantasy picks data for a gameweek
        Formatting done in output:
            - fill null values in chance_of_playing with 100
            - divide all costs by 10 to get costs as float as shown in web
            - get actual event points (depending on captaincy) rather than base event points
            - set player role in team in "role"
            - set player playing position in "field_position"
    """

    team_id = None
    # for convenience
    gameweek = None
    coreAPI = None


    def __init__(self,team_id,gameweek=None):
        if gameweek is None:
            gameweek = 2    #if no gameweek provided, set to current gameweek
        self.gameweek = gameweek
        self.team_id = team_id
        self.coreAPI = CoreAPI()


    def get_picks_data(self,gameweek=None):
        if gameweek is None:
            gameweek = self.gameweek
        picks_data = self.coreAPI.get_user_gameweek_picks_data(self.team_id,gameweek)
        picks_data = picks_data['picks']
        picks_data = sorted(picks_data, key=itemgetter('element'))  
        element_ids = [each_data['element'] for each_data in picks_data]
        brief_player_data = self.get_brief_player_data(element_ids)   
        # merging picks data and extra player data
        temp=[]
        for ctd,mtd in zip(picks_data,brief_player_data):
            temp.append({**ctd,**mtd})
        picks_data = sorted(temp, key=itemgetter('position'))
        # formatting output fields
        for i in range(len(picks_data)):
            # sometimes player is fit but chance_of_playing_next_round is null
            if(picks_data[i]['chance_of_playing_next_round'] is None):
                picks_data[i]['chance_of_playing_next_round'] = 100
            # costs are stored as integers - 6.1 is stored as 61
            picks_data[i]['now_cost'] = picks_data[i]['now_cost']/10
            picks_data[i]['cost_change_event'] = picks_data[i]['cost_change_event']/10
            picks_data[i]['event_points'] = picks_data[i]['event_points']*picks_data[i]['multiplier']
            # role
            if(picks_data[i]['is_captain']):
                role = "(C)"
            elif(picks_data[i]['is_vice_captain']):
                role = "(VC)"
            else:
                role = ""
            if(picks_data[i]['position']>11):
                role += "(Bench)"
            picks_data[i]['role'] = role
            # playing position
            if(picks_data[i]['element_type']==1):
                field_position = "GKP"
            elif(picks_data[i]['element_type']==2):
                field_position = "DEF"
            elif(picks_data[i]['element_type']==3):
                field_position = "MID"
            elif(picks_data[i]['element_type']==4):
                field_position = "FWD"
            picks_data[i]['field_position'] = field_position
        return picks_data


    def get_brief_player_data(self,element_ids):

        """
        Get some more player data for element ids

        Some of the player data is stored in links.FPL_DATA; linked to links.USER_GAMEWEEK_PICKS_DATA by element_id
        """

        fpl_data = self.coreAPI.get_fpl_data()
        brief_player_data = [each_data for each_data in fpl_data['elements'] if each_data['id'] in element_ids]
        brief_player_data = sorted(brief_player_data, key=itemgetter('id'))
        return brief_player_data


    def get_entry_data(self,gameweek=None):
         # if no gameweek provided, set to self.gameweek
        if gameweek is None:
            gameweek = self.gameweek
        # fetch all needed data
        entry_plus_league_data = self.coreAPI.get_user_data(self.team_id)
        entry_data = entry_plus_league_data['entry']
        return entry_data