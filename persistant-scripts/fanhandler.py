# The MIT License (MIT)

# Copyright (c) 2015 Prashant Nandipati (prashantn@riseup.net)

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.


import requests
from time import sleep
from json import dumps

ENDPOINT = 'http://192.168.1.10:8123/api/'
ENDPOINT_STATE = ENDPOINT + "states/"
ENDPOINT_SERVICE = ENDPOINT + 'services/switch/'
PIN_14 = "switch.fan_back_pin_14"
PIN_25 = "switch.fan_back_pin_25"
HEADERS = {'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIyNjI0NzBhNDJhMWY0ZDg3ODIxMzk3Njk1OTI0YjliOCIsImlhdCI6MTY1OTk1NzUwMCwiZXhwIjoxOTc1MzE3NTAwfQ.9q2mesUWFtKIul_j05IevjUVMf-GXQUg_saBTeTPo5I','content-type':'application/json',}

def set_state(url:str,state):
    payload = {'entity_id':url}
    url = ENDPOINT_SERVICE + 'turn_on' if (state == "on") else ENDPOINT_SERVICE + 'turn_off'
    print(payload,url)
    x = requests.post(
        url=url,
        data=dumps(payload),
        headers=HEADERS
    )
    print(x)
while True:
    fan_slider_val = float(requests.get(ENDPOINT_STATE+'input_number.slider1', headers=HEADERS).json()['state'])
    if(fan_slider_val < 10):
        set_state(PIN_14,"off")
        set_state(PIN_25,"off")
    elif(fan_slider_val < 40):
        set_state(PIN_14,"on")
        set_state(PIN_25,"off")
    elif(fan_slider_val < 70):
        set_state(PIN_14,"off")
        set_state(PIN_25,"on")
    elif(fan_slider_val >= 70):
        set_state(PIN_14,"on")
        set_state(PIN_25,"on")
    else:
        set_state(PIN_14,"off")
        set_state(PIN_25,"off")
    sleep(0.5)
