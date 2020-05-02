import requests
http_proxy = "http://kideveloper612:{API_KEY}@proxy.packetstream.io:31112"
https_proxy = "http://kideveloper612:{API_KEY}@proxy.packetstream.io:31112"
url = "https://ifconfig.co/json"

proxyDict = {
"http" : http_proxy,
"https" : https_proxy,
}

r = requests.get(url, proxies=proxyDict)