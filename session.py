import requests

def createSession():
    s = requests.Session()
    return s

def createTorSession():
    s = requests.Session()
    s.proxies = {'http': 'socks5h://127.0.0.1:9150',
                'https': 'socks5h://127.0.0.1:9150'}
    if s.get("http://httpbin.org/ip").text == requests.get("http://httpbin.org/ip").text:
        print("Unable to connect to the Tor network, quitting.")
        return False
    print("Created Tor session.")
    return s