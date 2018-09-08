import json
from operator import itemgetter
from .api_wrapper import ExtendedAPI


def set_default(func,*argv):
    def wrapper(team_id=argv[0],gameweek=argv[1]):
        return func(team_id,gameweek)
    return wrapper


class FPL(ExtendedAPI):
    """
    Importable FPL class containing all user accessible methods. Each instance is bound to a team_id at init
    """

    def __init__(self,team_id,gameweek=None):
        # set necessary defaults (team_id mandatory)
        if gameweek is None:
            gameweek = self.get_user_entry(team_id)['current_event']
        self.gameweek = gameweek
        self.team_id = team_id
        # now decorate all methods
        method_list = [x for x in dir(self) if callable(getattr(self,x)) and not x.startswith("_")]
        for method_name in method_list:
            setattr(self, method_name, set_default(getattr(self,method_name),self.team_id,self.gameweek))


    def get_user_gameweek_team_picks(self,team_id=None,gameweek=None,*argv):
        """
        Param:
        ------
        gameweek - default current week else given week

        Description:
        ------------
        Get detailed fantasy picks data for a gameweek.
        Formatting done in output:
            - fill null values in chance_of_playing with 100
            - divide all costs by 10 to get costs as float (as shown in web)
            - get actual event points (depending on multipliers) rather than base event points
            - set player role in team in "role"
            - set player playing position in "field_position"
        """
        picks_data = super().get_user_gameweek_team_picks(team_id,gameweek)
        picks_data = sorted(picks_data, key=itemgetter('element'))  
        element_ids = [each_data['element'] for each_data in picks_data]
        brief_player_data = self._get_brief_player_data(element_ids=element_ids)   
        # merging picks data and extra player data
        for ctd,mtd in zip(picks_data,brief_player_data):
            ctd.update(mtd)
        picks_data = sorted(picks_data, key=itemgetter('position'))
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

    

    def _get_brief_player_data(self,element_ids):

        """
        Get some more player data for element ids

        Some of the player data is stored in links.FPL_DATA; linked to links.USER_GAMEWEEK_PICKS_DATA by element_id
        """

        fpl_elements_data = self.get_fpl_elements()
        brief_player_data = [each_data for each_data in fpl_elements_data if each_data['id'] in element_ids]
        brief_player_data = sorted(brief_player_data, key=itemgetter('id'))
        return brief_player_data


    def get_entry_data(self,team_id=None,gameweek=None):
         # if no gameweek provided, set to self.gameweek
        if gameweek is None:
            gameweek = self.gameweek
        # fetch all needed data
        entry_plus_league_data = self.get_user_data(self.team_id)
        entry_data = entry_plus_league_data['entry']
        return entry_data


    """
    modify inherited methods
    """
    def get_user_gameweek_team_active_chip(self,team_id,gameweek,*argv):
        """ sets - actual name of active chip """
        active_chip_name = {"wildcard":"Wildcard","freehit":"Free Hit","bboost":"Bench Boost","3xc":"Triple Captain","":"-"}
        active_chip = super().get_user_gameweek_team_active_chip(team_id,gameweek)
        return active_chip_name[active_chip]

    def get_user_leagues(self,team_id,*argv):
        """ adds - entry_movement_symbol """
        entry_movement_symbol = {"up":"⮝","down":"⮟","same":"⚬","new":" "}
        leagues = super().get_user_leagues(team_id)
        for league_type in leagues:
            for each_league in leagues[league_type]:
                 each_league['entry_movement_symbol'] = entry_movement_symbol[each_league["entry_movement"]]
        return leagues