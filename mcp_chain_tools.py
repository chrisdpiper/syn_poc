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
    "X-Api-Key" : "65855c4b6926486393fd4f1a96f99972"
}

SERVER_URL = "https://api.songhub.certichain.synovient.com/api/v1"

async def get_chains_owned() -> str:
    """Get the ids of all chains owned.
    Args:
        none
    """
    print('syn::getting chains', file=sys.stderr)
  
    url = f"{SERVER_URL}/chains/"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
     #  print(response.text)
        response_json = response.json()
        data = response_json
    else:
        print(f"Error: {response.status_code}")
    return data



async def get_chain_links(chain_id: str) -> str:
    """Get links from a chain.

    Args:
        chain_id: the id of the chain
    """

    url = f"{SERVER_URL}/chains/" + chain_id + "/links"
    print('syn::getting chainlinks for ' + chain_id, file=sys.stderr)

      
    response = requests.get(url, headers=headers)
 #   print("sent response", file=sys.stderr_)
    if response.status_code == 200:
        print("syn::getting chainlinks response" + str(response), file=sys.stderr)

        response_json = response.json()
        #print("syn::getting chainlinks response" + str(response_json), file=sys.stderr)
        data = response_json.get("data")
        data_dict = dict(enumerate(data))
      
    else:
        print(f"syn::: response Error: {response.status_code}",file=sys.stderr)
        data = f"Error: {response.status_code}"
        
    return data_dict


async def get_chain_link_data(chain_id: str, link_id: str) -> str:
    """Get data from a linkof a chain.

    Args:
        chain_id: id of the chain
        link_id: id of the link
    """

    url = f"{SERVER_URL}/chains/" + chain_id + "/data/link/" + link_id
    print('syn::getting link data from ' + chain_id +  "link " + link_id, file=sys.stderr)

      
    response = requests.get(url, headers=headers)
 #   print("sent response", file=sys.stderr_)
    if response.status_code == 200:
        print("syn::getting chainlinks response" + str(response), file=sys.stderr)

        response_json = response.json()
        #print("syn::getting chainlinks response" + str(response_json), file=sys.stderr)
        data = response_json.get("data")
        data_dict = dict(enumerate(data))
      
    else:
        print(f"syn::: response Error: {response.status_code}",file=sys.stderr)
        data = f"Error: {response.status_code}"
        
    return data_dict



if __name__ == "__main__":
   # data = asyncio.run(get_chains_owned())
    
    #data = asyncio.run(get_chain_links('inventory-tracking-chain'))
    data = asyncio.run(get_chain_link_data('inventory-tracking-chain', 'lZWjOGbF6Xy-4hJEE_6iTXr5QYPpUz4JjdlKuOhVfow'))
    print("data:"+str(data))