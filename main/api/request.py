from configparser import ConfigParser
import requests
import json

config = ConfigParser()
config.read('config.ini')

class ApiRequest():
    def __init__(self):
        if config.has_section('api'):
            self.email = config.get('api', 'email')
            self.key = config.get('api', 'key')
        else:
            raise Exception("You haven't added your credentials yet. Login: cbcli login <email> <apikey>")
    
    def request(self, **kwargs):
        postData = {}  
        postData["email"] = self.email
        postData["secret"] = self.key
        for key, value in kwargs.items():
            postData[key] = value
        
        for key, value in postData.items():
            print("%s == %s" % (key, value))

        req = requests.post("https://api.combahton.net/v2", json = postData)
        return req
