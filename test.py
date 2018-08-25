import terminaltables
import json
from miniFPL import FPL


def make_table(data,header_names,json_keys,title=None):
    no_of_columns = len(header_names)
    no_of_rows = len(data)
    
    rows=[header_names]
    rows.extend([ [each[json_keys[i]] for i in range(no_of_columns)] for each in data ])

    table = terminaltables.SingleTable(table_data=rows,title=title)
    for i in range(no_of_columns):
        table.justify_columns[i]="center" 
    return table.table


if __name__=="__main__":
    team_id = input("Enter the team id: ")
    obj = FPL(team_id)

    # User Details
    data = [obj.get_user_entry(team_id)]
    header_names = ["Name","Team","Region","Gameweek Points"]
    json_keys = ["player_full_name","name",'player_region_name','summary_event_points']
    table = make_table(data,header_names,json_keys,title="User")
    print(table)

    # Team Details
    data = json.loads(obj.get_picks_data())
    header_names = ["Position","Name","Role","Points","News"]
    json_keys = ["field_position",'web_name','role','event_points','news']
    table = make_table(data,header_names,json_keys,title="Team")
    print(table)
