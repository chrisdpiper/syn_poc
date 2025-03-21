'''
Copyright [2025] Ambient Enterprises Technologies, Inc.
All rights reserved.

This software is licensed under Ambient Enterpries LLC. You may obtain a copy of the Licensing and Privacy Policy at:
* Ambient Enterprises Terms and Conditions ("Ambient T&C")[https://ambiententerprises.com/ambient-enterprises-terms-and-conditions-ambient-tc-2/]
* Ambient Enterprises User Master License (“UML”) : [https://ambiententerprises.com/ambient-user-master-license-uml-2/]
* Ambient Enterprises Privacy Policy: [https://ambiententerprises.com/privacy-policy/]

Redistribution in any form is not allowed, and modifications to the software are prohibited.

THIS SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import requests
import hashlib
import json
import re

# Prompt the user to input the file path
file_path = input("Enter the path to the file you want to upload: ").strip()

# Validate the file path
try:
    with open(file_path, "rb") as file:
        print(f"File '{file_path}' found.")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found!")
    exit(1)

# Extract DAC ID and server_url from the first 4KB of the file
try:
    with open(file_path, "rb") as file:
        first_4kb = file.read(4096).decode('utf-8', errors='ignore')  # Decode as UTF-8 with error handling
        
        # Use regex to extract the first JSON object containing "dac_id" and "server_url"
        match = re.search(r'\{.*?"dac_id"\s*:\s*".*?",.*?"server_url"\s*:\s*".*?".*?\}', first_4kb, re.DOTALL)
        if match:
            json_content = json.loads(match.group())  # Parse the matched JSON object
            dac_id = json_content.get("dac_id")
            server_url = json_content.get("server_url")
            if not dac_id or not server_url:
                print("Error: 'dac_id' or 'server_url' not found in the file's JSON content!")
                exit(1)
            print(f"DAC ID extracted from file: {dac_id}")
            print(f"Server URL extracted from file: {server_url}")
        else:
            print("Error: No valid JSON object containing 'dac_id' and 'server_url' found in the first 4KB of the file!")
            exit(1)
except Exception as e:
    print(f"Error reading or parsing the file for DAC ID or Server URL: {e}")
    exit(1)

# Use DAC ID as the file name with .dac extension
file_name = f"{dac_id}.dac"
print(f"Using DAC ID as file name: {file_name}")

# Prompt the user to input the JWT token
jwt_token = input("Enter your JWT token: ").strip()

if not jwt_token:
    print("Error: JWT token cannot be empty!")
    exit(1)

# API details for fetching upload link
upload_link_url = f"{server_url}/api/v1/dacs/upload_link"

# Function to calculate SHA-1 hash of a file
def calculate_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):  # Read in chunks to handle large files
            sha1.update(chunk)
    return sha1.hexdigest()

# Fetch the authorization token and upload URL
try:
    response = requests.get(
        upload_link_url,
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    if response.status_code == 200:
        upload_data = response.json()
        authorization_token = upload_data["authorizationToken"]
        upload_url = upload_data["uploadUrl"]
    else:
        print("Failed to fetch upload link.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to connect to the server: {e}")
    exit(1)

# Calculate the SHA-1 hash of the file
sha1_hash = calculate_sha1(file_path)

# Debug: Check if the `authorizationToken` is set
if not authorization_token:
    print("Error: Authorization token is missing or empty!")
    exit(1)

# Headers for the upload
headers = {
    "Authorization": authorization_token,
    "X-Bz-File-Name": f"/incoming/{file_name}",
    "Content-Type": "application/octet-stream",
    "X-Bz-Content-Sha1": sha1_hash,  # Dynamically calculated SHA-1 hash
}

# Debug: Check if the file exists and upload
try:
    with open(file_path, "rb") as file_data:
        # Send the file upload request
        response = requests.post(upload_url, headers=headers, data=file_data)

    # Output the response
    if response.status_code == 200:
        print("File uploaded successfully!")
        upload_response = response.json()
        file_id = upload_response.get("fileId")
        print(f"File ID: {file_id}")
        print(f"SHA1 Hash: {sha1_hash}")
    else:
        print("Failed to upload the file.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to connect to the server: {e}")
    exit(1)

# POST to register the upload
register_upload_url = f"{server_url}/api/v1/dacs/{dac_id}/register_upload"

payload = {
    "file_id": file_id,
    "sha1": sha1_hash
}

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(register_upload_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Upload registered successfully!")
        print("Response:", response)
    else:
        print("Failed to register the upload.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to connect to the server: {e}")
