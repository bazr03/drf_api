import requests

#endpoint = "http://httpbin.org/status/200/"
endpoint = "http://127.0.0.1:8000/api/products/"


data = {
    "title":"new title updated ",
    "price": 49.99
}

get_response = requests.post(endpoint, json=data)
#print(get_response.text) 
print(get_response.json()) 