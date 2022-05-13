import requests

#endpoint = "http://httpbin.org/status/200/"
endpoint = "http://127.0.0.1:8000/api/"

get_response = requests.post(endpoint, params={"abc":123}, json={"content": "Hello world", "title":"abc123", "price":299.9})
#print(get_response.text) 
print(get_response.json()) 