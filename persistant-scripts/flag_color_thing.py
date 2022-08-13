# The MIT License (MIT)

# Copyright (c) 2015 Prashant Nandipati (prashantn@riseup.net)
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

"""
Count the values like this on the tv (the led strips)

SEG_SPLIT = [0 , h/3 ,2h/3 , w + 2h/3 , w + 3h/3 , w + 4h/3 ]

       ┌─────────────── w──────────────┐
       │ ┌──────────────────────────┐  │
       ▼ │          Orange          │  ▼
   2h/3  │                          │  w + 2h/3
       ▲ ├──────────────────────────┤  ▲
       │ │                          │  │
       │ │          White           │  │
       ▼ │                          │  ▼
   h/3   ├──────────────────────────┤  w + 3h/3
       ▲ │                          │  ▲
       │ │          Green           │  │
       │ │                          │  │
    0  ▼ └──────────────────────────┘  ▼  w + 4h/3

"""
# ----- CONFIG ------ #
SEG_SPLIT = [0,3,6,33,36,50] # this is for my Monitor 

WLED_IP = "192.168.0.174" # check the ip for wled in lab 2  it's connected to SCRC_LAB_IOT


# -----  DATA  ------ #
HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
INDIAN_FLAG = {
    "state":{
        "on":True,
        "bri":127
    },
    "seg":[
        {
            "start":SEG_SPLIT[0],
            "stop":SEG_SPLIT[1],
            "len":SEG_SPLIT[1]-SEG_SPLIT[0],
            "col":[[19,136,8]]
        },
        {
            "start":SEG_SPLIT[1],
            "stop":SEG_SPLIT[2],
            "len":SEG_SPLIT[2]-SEG_SPLIT[1],
            "col":[[255,255,255]]
        },
        {
            "start":SEG_SPLIT[2],
            "stop":SEG_SPLIT[3],
            "len":SEG_SPLIT[3]-SEG_SPLIT[2],
            "col":[[255,153,51]]
        },
        {
            "start":SEG_SPLIT[3],
            "stop":SEG_SPLIT[4],
            "len":SEG_SPLIT[4]-SEG_SPLIT[3],
            "col":[[255,255,255]]
        },
        {
            "start":SEG_SPLIT[4],
            "stop":SEG_SPLIT[5],
            "len":SEG_SPLIT[5]-SEG_SPLIT[4],
            "col":[[19,136,8]]
        }
    ]
}

if(__name__ == "__main__"):
    import requests,json
    print("Posting to WLED JSON endpoint")
    response = requests.post("http://" + WLED_IP + "/json",headers=HEADERS,data=json.dumps(INDIAN_FLAG))
    if(response.status_code < 300):
        print(response.text)
