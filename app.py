from bottle import Bottle
from jinja2 import Environment,FileSystemLoader
import json
from miniFPL import FPL

app = Bottle()

@app.route('/<team_id>')
def hello(team_id):
    #team_id = input("Enter the team id: ")
    obj = FPL(team_id)

    header_names_list = []
    rows_list = []
    table_title_list = []
    # User Details
    data = [obj.get_user_entry(team_id)]
    header_names = ["Name","Team","Region","Gameweek Points"]
    json_keys = ["player_full_name","name",'player_region_name','summary_event_points']
    rows = [ [each[json_keys[i]] for i in range(len(header_names))] for each in data]
    header_names_list.append(header_names)
    rows_list.append(rows)
    table_title_list.append("User Details")

    # Team Details
    data = json.loads(obj.get_picks_data())
    header_names = ["Position","Name","Role","Points","News"]
    json_keys = ["field_position",'web_name','role','event_points','news']
    rows = [ [each[json_keys[i]] for i in range(len(header_names))] for each in data]
    header_names_list.append(header_names)
    rows_list.append(rows)
    table_title_list.append("Team Details")

    template_env = Environment(loader=FileSystemLoader(searchpath="./"))
    template = template_env.get_template("template.html")
    template = template.render(header_names=header_names_list,rows=rows_list,table_titles=table_title_list)

    return(template)

app.run()
