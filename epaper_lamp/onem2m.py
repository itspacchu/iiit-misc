# The MIT License (MIT)

# Copyright (c) 2015 Prashant Nandipati (prashantn@riseup.net)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from time import sleep
import requests
from random import randint


class Sensor:
    USRNAME,PASSWD = "guest","guest"
    IIIT_OM2M_URL_BASE = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/"

    OM2M_HEADERS = {
        'X-M2M-Origin': 'guest:guest',
        'Accept': 'application/json'
    }

    def __init__(self,nodeloc='',node=''):
        self.nodeloc = nodeloc
        self.node = node

    def FETCH_URL(self,node_loc="AE-SR",node_name="SR-AQ"):
        return f"{self.IIIT_OM2M_URL_BASE}{node_loc}/{node_name}/Data/la"

    def fetch_data(self,url:str):
        response = requests.get(url=url, headers=self.OM2M_HEADERS)
        if(response.status_code == 200):
            return response.json()
        else:
            return response.text
    
    def getData(self,enums=[]):
        try:
            rawList = self.fetch_data(self.FETCH_URL(self.nodeloc,self.node))['m2m:cin']['con']
            print(rawList)
            jsonDat = {}
            for i,data in enumerate(rawList[1:-1].split(',')[:len(enums)]):
                try:
                    jsonDat[enums[i]] = float(data)
                except ValueError:
                    jsonDat[enums[i]] = -1
            return jsonDat
        except ValueError:
            return {0}

    def remap(self,value,old_min,old_max,new_min,new_max):
        """
        Remap (value) ranging from (old_min to old_max) to (new_min to new_max)
        """
        return ((value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min



class SolarNode(Sensor): 
    def getData(self,enums=['Timestamp',"energy","power","voltage","current","frequency","pf"]):
        return super().getData(enums=enums)

class AirQuality(Sensor):
    def getData(self,enums=['Timestamp',"pm2_5","pm10","temp","rH","CO","NO2","NH3","AQI","AQL","AQI_MP","data_interval"]):
        return super().getData(enums=enums)

class WaterQuality(Sensor):
    def getData(self,enums=['Timestamp', 'Temperature', 'TDS_Voltage', 'Uncompensated_TDS_value', 'Compensated_TDS_value', 'Water_Level']):
        return super().getData(enums=enums)

class WaterFlow(Sensor):
    def getData(self,enums=['Timestamp', 'Flowrate', 'Total_Flow']):
        return super().getData(enums=enums)

if(__name__ == "__main__"):
    pass
