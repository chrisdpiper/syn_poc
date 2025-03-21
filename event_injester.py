
from events_db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
import time
import requests
import hashlib
import json
import os



# Server URL for easy change
SERVER_URL = "https://api.staging.certify.synovient.com/api/v1"

# Prompt user for credentials
user = "cpiper@synovient.com"
password = "P@ssw0rd_syn"

# Define headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiJjcGlwZXJAc3lub3ZpZW50LmNvbSIsIkZpcnN0TmFtZSI6ImNocmlzIiwiTGFzdE5hbWUiOiJwaXBlciIsImV4cCI6MTc0MjYxNTUzOX0.6BkycdeX8Dp7tLPnumr0ANmkDTvoVC7pSwtnLwBnh-GtfO5SgR3Ge4o9ArztF7EYBfijpckBAVBDZtWGepPkQA"
}


def get_dac_events(dac_id):
    url = f"{SERVER_URL}/dacs/"+ dac_id + "/events"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        #print(response.text)
        print("success")
        response_json = response.json()
        data = response_json.get("data")
    else:
        print(f"Error: {response.status_code}")
    return data



embedder = GPT4AllEmbeddings()
db = db_class(embedder)



script_start_time = time.time()

execution_times = []



#events = get_dac_events("b2a26427e1c74ad4b76a6572d6ba77f3.3d4c64fea95e40999de1c40c60799da6")
path = os.getcwd() + "\\raw_events"
#print("path:"+ path)
files = os.listdir(path)

for file in files:
         start_time = time.time()
         db.load(path+"\\"+file)
         end_time = time.time()
         execution_time = end_time - start_time
         print(f"url load time: {execution_time} seconds")
         execution_times.append(execution_time)






      

       


