import json
from datetime import datetime

# def convert_schedule_json_to_dict(json_data):
#     print("We been heerre")
#     return json.loads(json_data)


# with open('data.json', 'r') as file:
#     json_data = file.read()

# data = json.loads(json_data)
# print(data[0])

# start_time = data[0]['startTime']
# print("Start Time:", start_time)

# datetime_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')

# formatted_time = datetime_obj.strftime('%H:%M')

# print("Formatted Time:", formatted_time)

import requests
import json

def fetch_data_and_save_to_file(url, output_file):
    # Make a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Write the JSON data to a file
        with open(output_file, 'w') as file:
            json.dump(data, file)
        
        print("Data saved to", output_file)
    else:
        print("Failed to fetch data from", url, ". Status code:", response.status_code)

# Example usage:
url1 = "https://ap-southeast-1.aws.data.mongodb-api.com/app/application-0-ssvkjuv/endpoint/fetchArea"
output_file1 = "./data/area-selector.json"
fetch_data_and_save_to_file(url1, output_file1)

url2 = "https://ap-southeast-1.aws.data.mongodb-api.com/app/application-0-ssvkjuv/endpoint/fetchScheduler"
output_file2 = "./data/scheduler.json"
fetch_data_and_save_to_file(url2, output_file2)

with open('./data/area-selector.json', 'r') as file:
    json_data = file.read()

data = json.loads(json_data)
# for item in data:
#     item['onSchedule'] = False
# print(len(data))
print(data["area1"])


# start_time = data[0]['startTime']
# print("Start Time:", start_time)

# datetime_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')

# formatted_time = datetime_obj.strftime('%H:%M')

# print("Formatted Time:", formatted_time)


# import time
# from datetime import datetime

# print("TESTING")

# now = datetime.now()
# print(now)
# current_time = now.strftime("%H:%M")
# print(current_time)
