import json
from collections import OrderedDict
import prettytable
from miniFPL import FPL

team_id = input("Enter the team id: ")
obj = FPL(team_id)

data = obj.get_picks_data()

headers = ["Position","Name","Role","Points","News"]
json_keys = ['field_position','web_name','role','event_points','news']

no_of_columns = len(headers)
columns = [ [each[json_keys[i]] for each in data] for i in range(no_of_columns) ]

table = prettytable.PrettyTable()
for i in range(no_of_columns):
    table.add_column(headers[i],columns[i])

print(table)
