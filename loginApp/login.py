import requests

url = "http://127.0.0.1:8000/api/signup/"
data = {
   
    "username": "Sunibalan",
    "emai id":"sunibalan123@gmail.com",
    "password": "Suni_Balan@3"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())

