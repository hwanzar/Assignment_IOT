import json
def convert_schedule_json_to_dict(json_data):
    print("We been heerre")
    return json.loads(json_data)


with open('data.json', 'r') as file:
    json_data = file.read()


