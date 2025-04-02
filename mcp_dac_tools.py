from textwrap import dedent
import httpx
from typing import Any
import logging
import time
import requests
import hashlib
import json
import os
import asyncio
import sys



# Define headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiJjcGlwZXJAc3lub3ZpZW50LmNvbSIsIkZpcnN0TmFtZSI6ImNocmlzIiwiTGFzdE5hbWUiOiJwaXBlciIsImV4cCI6MTc0MzYyMTM3M30.fuEiEHz6VHEdHJ17q4BnfuZH6rJbFHjp4b4TRUzZmONrtdumKBFGEWR1e6UZBuo-9abdlH_uGTd96nOVmnE-AA"
}

async def get_dac_events(dac_id: str) -> str:
    """Get events from a dac.

    Args:
        dac_id: guid like id 
    """
    SERVER_URL = "https://api.staging.certify.synovient.com/api/v1"
    url = f"{SERVER_URL}/dacs/"+ dac_id + "/events?limit=5000"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        #print(response.text)
        response_json = response.json()
        data = response_json.get("data")
    else:
        print(f"Error: {response.status_code}")
    return data



async def get_dacs_owned() -> str:
    """Get the ids of all dacs owned.
    Args:
        none
    """
    url = "https://api.staging.certify.synovient.com/api/v1/dacs/owned"
    #url = "https://test.com"


      
    response = requests.get("https://api.staging.certify.synovient.com/api/v1/dacs/owned", headers=headers)
 #   print("sent response", file=sys.stderr_)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get("data")
        data_dict = dict(enumerate(data))
    #    print("got response" + str(data_dict))
    else:
        print(f"Error: {response.status_code}")
        data = f"Error: {response.status_code}"
        
        #print("got error response", file=sys.stderr_)
    

    
  #  return dedent(
   #     f"""
    #    count: {data_dict.get('total_count', 'Unknown')}
     #   ID: {data_dict.get('dav_id', 'Unknown')}
      #  Name: {data_dict.get('name', 'Unknown')}
       # Description: {data_dict.get('description', 'No description available')}

        #"""
    #)
    #data = "no data"
    return data_dict



if __name__ == "__main__":
    #Run the server
    data = asyncio.run(get_dacs_owned())
    print("data:"+str(data))