# https://github.com/itspacchu/iiit-automation-scripts/blob/main/ha_sensor/onem2m.py

from time import sleep
import requests
from random import randint

class Sensor:
    USRNAME,PASSWD = "guest","guest"
    IIIT_OM2M_URL_BASE = "https://dev-onem2m.iiit.ac.in:443/~/in-cse/in-name/"

    OM2M_HEADERS = {
        'X-M2M-Origin': 'guest:guest',
        'Accept': 'application/json'
    }

    def FETCH_URL(self,node_loc="AE-SR",node_name="SR-AQ"):
        return f"{self.IIIT_OM2M_URL_BASE}{node_loc}/{node_name}/Data/la"

    def fetch_data(self,url:str):
        response = requests.get(url=url, headers=self.OM2M_HEADERS)
        if(response.status_code == 200):
            return response.json()
        else:
            return response.text

    def remap(self,value,old_min,old_max,new_min,new_max):
        """
        Remap (value) ranging from (old_min to old_max) to (new_min to new_max)
        """
        return ((value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

class SolarNode(Sensor):
    def __init__(self,nodeloc,node):
        self.nodeloc = nodeloc
        self.node = node
    
    def getData(self):
        enums = ["unix_time","energy","power","voltage","current","frequency","pf"]
        try:
            rawList = self.fetch_data(self.FETCH_URL(self.nodeloc,self.node))['m2m:cin']['con']
            jsonDat = {}
            for i,data in enumerate(rawList[1:-1].split(',')[:6]):
                try:
                    jsonDat[enums[i]] = float(data)
                except ValueError:
                    jsonDat[enums[i]] = -1
            return jsonDat
        except ValueError:
            return {0}

if(__name__ == "__main__"):
    pass