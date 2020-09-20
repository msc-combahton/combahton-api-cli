from configparser import ConfigParser
import requests
import json

import logging
logger = logging.getLogger(__name__)

config = ConfigParser()
config.read('config.ini')

class ApiRequest():
    def __init__(self):
        if config.has_section("core"):
            if config.has_option("core","verbosity"):
                logger.setLevel(logging.getLevelName(config.get("core","verbosity")))
        pass
    
    def request(self, **kwargs):
        if config.has_section('user'):
            self.email = config.get('user', 'email')
            self.key = config.get('user', 'key')
        else:
            raise Exception("You haven't added your credentials yet.\nPlease provide your API credentials, use:\n\tcbcli config set user.email <email>\n\tcbcli config set user.key <api-key>")

        postData = {}  
        postData["email"] = self.email
        postData["secret"] = self.key
        for key, value in kwargs.items():
            postData[key] = value
        
        logger.debug("[Verbose] Follwing data will be sent:")
        for key, value in postData.items():
            logger.debug("%s == %s" % (key, value))

        req = requests.post("https://api.combahton.net/v2", json = postData)
        return req
