import requests

ip = '127.0.0.1'
port = ":5000"
path = '/v1/test'
endpoint = 'http://' + ip + port + path 
r = requests.get(endpoint)
print(r.text)
