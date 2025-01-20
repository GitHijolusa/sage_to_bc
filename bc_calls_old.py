import requests
from requests_ntlm import HttpNtlmAuth
import json

def bc_connect(url, username, password, data):
    headers = {
        'Content-Type': 'application/json'
    }
    auth = HttpNtlmAuth(username, password)
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
    try:
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        print(f"Response content: {response.text}")

# Example usage
url = "http://sql-nav-pre:7048/BC_Test/ODataV4/Company('AGRICOLA%20VILLENA%20SL')/Empleados"  # Replace with your actual endpoint
username = "SQL-NAV-PRE\\ALFREDO.BLANCO"  # Replace with your Business Central username. Note the double backslash.
password = "Rol62357"  # Replace with your Business Central password

# Sample data for the post request.  Adapt this to your specific needs.
data = {
    "No": "0001",
    "Name": "John",
    "First_Family_Name": "Doe"
}
print(username)
response = bc_connect(url, username, password, data)
print(response)
