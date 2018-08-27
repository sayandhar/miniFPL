import requests
from .api_url import *


class CoreAPI:
    """
    Getters for json data directly from official FPL links
    """

    def __init__(self):
        pass


    def get_fpl_data(self):
        try:
            fpl_data = requests.get(FPL_DATA).json()
        except requests.exceptions.SSLError:
            fpl_data = requests.get(FPL_DATA,verify=False).json()
        return fpl_data


    def get_player_data(self,player_id):
        try:
            player_data = requests.get(PLAYER_DATA.format(player_id)).json()
        except requests.exceptions.SSLError:
            player_data = requests.get(PLAYER_DATA.format(player_id),verify=False).json()
        return player_data


    def get_dream_team_data(self,gameweek):
        try:
            dream_team_data = requests.get(PLAYER_DATA.format(gameweek)).json()
        except requests.exceptions.SSLError:
            dream_team_data = requests.get(PLAYER_DATA.format(gameweek),verify=False).json()
        return dream_team_data


    def get_user_gameweek_team_data(self,team_id,gameweek):
        try:
            user_gameweek_team_data = requests.get(USER_GAMEWEEK_TEAM_DATA.format(team_id,gameweek)).json()
        except requests.exceptions.SSLError:
            user_gameweek_team_data = requests.get(USER_GAMEWEEK_TEAM_DATA.format(team_id,gameweek),verify=False).json()
        return user_gameweek_team_data


    def get_user_data(self,team_id):
        try:
            user_data = requests.get(USER_DATA.format(team_id)).json()
        except requests.exceptions.SSLError:
            user_data = requests.get(USER_DATA.format(team_id),verify=False).json()
        return user_data


class ExtendedAPI(CoreAPI):
    """
    Separate methods to parse the JSON from CoreAPI()
    """

    def __init__(self):
        super.__init__()


    """ 
    for self.get_fpl() 
    """
    def get_fpl_elements(self):
        elements = self.get_fpl_data()['elements']
        return elements

    def get_fpl_phases(self):
        phases = self.get_fpl_data()['phases']
        return phases

    def get_fpl_events(self):
        events = self.get_fpl_data()['events']
        return events

    
    """
    for self.get_user_gameweek_team()
    """
    def get_user_gameweek_team_picks(self,team_id,gameweek):
        picks = self.get_user_gameweek_team_data(team_id,gameweek)['picks']
        return picks

    def get_user_gameweek_team_active_chip(self,team_id,gameweek):
        active_chip = self.get_user_gameweek_team_data(team_id,gameweek)['active_chip']
        return active_chip
    
    def get_user_gameweek_team_automatic_subs(self,team_id,gameweek):
        automatic_subs = self.get_user_gameweek_team_data(team_id,gameweek)['automatic_subs']
        return automatic_subs

    def get_user_gameweek_team_event(self,team_id,gameweek):
        event = self.get_user_gameweek_team_data(team_id,gameweek)['event']
        return event

    def get_user_gameweek_team_entry_history(self,team_id,gameweek):
        entry_history = self.get_user_gameweek_team_data(team_id,gameweek)['entry_history']
        return entry_history

    
    """
    for self.get_user_data()
    """
    def get_user_entry(self,team_id):
        entry = self.get_user_data(team_id)['entry']
        entry['player_full_name'] = entry['player_first_name']+" "+entry['player_last_name']
        return entry
