from bottle import Bottle, request
from jinja2 import Environment,FileSystemLoader
from collections import OrderedDict
import json
from miniFPL import FPL

app = Bottle()

@app.get('/')
def hello():
    team_id = request.params.get('team_id')
    template_env = Environment(loader=FileSystemLoader(searchpath="./"))
    # if no team_id is present, return the home page
    if team_id is None:
        template = template_env.get_template("index.html")
        template = template.render()
        return template
    # else, return the stats for the team_id
    obj = FPL(team_id)

    left_headers = []
    left_rows = []
    table_title_list = []

    user_entry = obj.get_user_entry(team_id)
    gw = obj.get_user_entry(team_id)['current_event']
    user_leagues = obj.get_user_leagues(team_id)
    entry_history = obj.get_user_gameweek_team_entry_history(team_id,gw)
    event = obj.get_user_gameweek_team_event(team_id,gw)
    active_chip = obj.get_user_gameweek_team_active_chip(team_id,gw)

    ################################################################################
    ## USER INFO
    ################################################################################
    header_names = ["Name","Team","Region","Overall Pts","Overall Rank","Value","Bank"]
    rows = [[
        user_entry['player_first_name']+" "+user_entry['player_last_name'],
        user_entry['name'],
        user_entry['player_region_short_iso'],
        "{:,}".format(user_entry['summary_overall_points']),
        "{:,}".format(user_entry['summary_overall_rank']),
        '£'+str(user_entry['value']/10),
        '£'+str(user_entry['bank']/10),
    ]]
    left_headers.append(header_names)
    left_rows.append(rows)
    table_title_list.append("User Details")

    ################################################################################
    ## GAMEWEEK
    ################################################################################
    active_chip_name={"wildcard":"Wildcard","freehit":"Free Hit","bboost":"Bench Boost","3xc":"Triple Captain","":"-"}
    header_names = ["GW Pts","Transfer Cost","Average Pts","Highest Pts","GW Rank","Active Chip"]
    rows = [[
        entry_history['points'], 
        -1*entry_history['event_transfers_cost'], 
        event['average_entry_score'], 
        event['highest_score'],
        "{:,}".format(entry_history['rank']),
        active_chip_name[active_chip]
        ]]
    left_headers.append(header_names)
    left_rows.append(rows)
    table_title_list.append(event['name'])

    ################################################################################
    ## TEAM
    ################################################################################
    data = json.loads(obj.get_picks_data())
    header_names = ["Position","Name","Role","Points","Cost","News"]
    json_keys = ["field_position",'web_name','role','event_points','now_cost','news']
    rows = [ [each[json_keys[i]] for i in range(len(header_names))] for each in data]
    left_headers.append(header_names)
    left_rows.append(rows)
    table_title_list.append("Team Details")

    ################################################################################
    ## LEAGUES
    ################################################################################
    league_tables = OrderedDict()
    league_headers = ["ID","League Name","Current Rank","Last Rank","Change"]
    json_keys = ["id","name","entry_rank","entry_last_rank","entry_movement"]
    entry_movement_symbol = {"up":"🠉","down":"🠋","same":"●","new":"new"}

    h2h = user_leagues['h2h']
    classic = user_leagues['classic']
    
    for each in h2h:
        each['entry_movement'] = entry_movement_symbol[each["entry_movement"]]
    for each in classic:
        each['entry_movement'] = entry_movement_symbol[each["entry_movement"]]  

    league_tables["Head-to-Head Leagues"] = [ [each[key] for key in json_keys] for each in h2h]
    league_tables["Classic Leagues"] = [ [each[key] for key in json_keys] for each in classic if each['league_type']!='s']
    league_tables["Global Leagues"] = [ [each[key] for key in json_keys] for each in classic if each['league_type']=='s']  
    

    template_env = Environment(loader=FileSystemLoader(searchpath="./"))
    template = template_env.get_template("results.html")
    template = template.render(
        left_headers=left_headers,
        left_rows=left_rows,
        table_titles=table_title_list,
        league_headers=league_headers,
        league_tables=league_tables
        )

    return template

app.run()
