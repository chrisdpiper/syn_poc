import requests
import hashlib
import json
import os
# Server URL for easy change
SERVER_URL = "https://api.staging.certify.synovient.com/api/v1"

# Prompt user for credentials
user = "cpiper@synovient.com"
password = "P@ssw0rd_syn"



# Define the request body
body = {
    "user_id": user,
    "password": password,
#    "challenge": hashed_value
}
json_body = json.dumps(body)

# Define headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiJjcGlwZXJAc3lub3ZpZW50LmNvbSIsIkZpcnN0TmFtZSI6ImNocmlzIiwiTGFzdE5hbWUiOiJwaXBlciIsImV4cCI6MTc0MjYxNTUzOX0.6BkycdeX8Dp7tLPnumr0ANmkDTvoVC7pSwtnLwBnh-GtfO5SgR3Ge4o9ArztF7EYBfijpckBAVBDZtWGepPkQA"

}
# Define API URL for lhistory
#b2a26427e1c74ad4b76a6572d6ba77f3.3d4c64fea95e40999de1c40c60799da6
dac_id = "b2a26427e1c74ad4b76a6572d6ba77f3.f43b953653224bd39d069419b05da6c6"
history_url = f"{SERVER_URL}/dacs/"+ dac_id + "/events"
print (history_url)


# Send POST request for login
def get_dac_events(dac_id):
    url = f"{SERVER_URL}/dacs/"+ dac_id + "/events"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        #print(response.text)
        print("success")
        response_json = response.json()
        data = response_json.get("data")
        for event in data:
            print("*"*30)
            event_json = json.loads(json.dumps(event))
            print(event_json.get("event_id"))
            subfolder_name = "raw_events"
            file_name = event_json.get("event_id") + ".txt"
            file_path = os.path.join(subfolder_name, file_name)
            with open(file_path, "w") as outfile:
                outfile.write(str(event_json))
    else:
        print(f"Error: {response.status_code}")


def get_dac_owned():
    url = f"{SERVER_URL}/dacs/owned"
    response = requests.get(url, headers=headers)
    #response.raise_for_status()
    if response.status_code == 200:
        #print(response.text)
        print("success")
        response_json = response.json()
        dacs = response_json.get("data")
        for dac in dacs:
            print(dac)
    else:
        print(f"Error: {response.status_code}")
    



#get_dac_owned()
get_dac_events("b2a26427e1c74ad4b76a6572d6ba77f3.3d4c64fea95e40999de1c40c60799da6")

