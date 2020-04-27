import requests
url = 'https://httpbin.org/ip'
proxies = {
    "http": 'http://109.111.171.49:3128',
    "https": 'https://109.111.171.49:3128'
}
response = requests.get(url, proxies=proxies)
print(response.json())
