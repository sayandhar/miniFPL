from bottle import Bottle, request
from jinja2 import Environment,FileSystemLoader
import json
from miniFPL import FPL

app = Bottle()

@app.get('/')
def hello():
    #team_id = input("Enter the team id: ")
    team_id = request.params.get('team_id')
    obj = FPL(team_id)

    header_names_list = []
    rows_list = []
    table_title_list = []

    user_entry = obj.get_user_entry()
    entry_history = obj.get_user_gameweek_team_entry_history(team_id,3)
    event = obj.get_user_gameweek_team_event(team_id,3)
    active_chip = obj.get_user_gameweek_team_active_chip(team_id,3)

    # User Details
    header_names = [
        "Name",
        "Team",
        "Region",
        "Overall Pts",
        "Overall Rank",
        "Value",
        "Bank"
        ]
    rows = [[
        user_entry['player_full_name'],
        user_entry['name'],
        user_entry['player_region_short_iso'],
        "{:,}".format(user_entry['summary_overall_points']),
        "{:,}".format(user_entry['summary_overall_rank']),
        '£'+str(user_entry['value']/10),
        '£'+str(user_entry['bank']/10),
    ]]
    header_names_list.append(header_names)
    rows_list.append(rows)
    table_title_list.append("User Details")


    # Gameweek
    header_names = [
        "GW Pts",
        "Transfer Cost",
        "Average Pts",
        "Highest Pts",
        "GW Rank",
        "Active Chip"
        ]
    rows = [[
        entry_history['points'], 
        -1*entry_history['event_transfers_cost'], 
        event['average_entry_score'], 
        event['highest_score'],
        "{:,}".format(entry_history['rank']),
        active_chip
        ]]
    header_names_list.append(header_names)
    rows_list.append(rows)
    table_title_list.append(event['name'])


    # Team Details
    data = json.loads(obj.get_picks_data())
    header_names = ["Position","Name","Role","Points","Cost","News"]
    json_keys = ["field_position",'web_name','role','event_points','now_cost','news']
    rows = [ [each[json_keys[i]] for i in range(len(header_names))] for each in data]
    header_names_list.append(header_names)
    rows_list.append(rows)
    table_title_list.append("Team Details")

    template_env = Environment(loader=FileSystemLoader(searchpath="./"))
    template = template_env.get_template("template.html")
    template = template.render(header_names=header_names_list,rows=rows_list,table_titles=table_title_list)

    return(template)

app.run()
