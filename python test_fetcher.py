import requests

data = {
    "roll": "23BIT005",
    "password": "hicas",
    "dob": "29-07-2005"
}

res = requests.post("http://127.0.0.1:5000/login", json=data)
print(res.json())
