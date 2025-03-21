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

# Server URL for easy change
SERVER_URL = "https://api.staging.certify.synovient.com/api/v1"

# Prompt user for credentials
user = input("Enter your username: ")
password = input("Enter your password: ")

# Define the API URL for work challenge
work_challenge_url = f"{SERVER_URL}/auth/work-challenge"

# Send GET request to fetch challenge
def fetch_challenge():
    response = requests.get(work_challenge_url)
    response.raise_for_status()
    return response.json()

data = fetch_challenge()
challenge = data["challenge"]
iterations = int(data["iterations"])

# Perform the hashing iterations
hashed_value = challenge
for _ in range(iterations):
    hashed_value = hashlib.sha256(hashed_value.encode()).hexdigest()

# Define API URL for login
login_url = f"{SERVER_URL}/auth/login"

# Define the request body
body = {
    "user_id": user,
    "password": password,
    "challenge": hashed_value
}
json_body = json.dumps(body)

# Define headers
headers = {
    "Content-Type": "application/json"
}

# Send POST request for login
def login():
    response = requests.post(login_url, headers=headers, data=json_body)
    response.raise_for_status()
    return response.json()

login_response = login()
jwt = login_response.get("jwt")

# Output the JWT
echoed_jwt = f"JWT Token: {jwt}"
print(echoed_jwt)
