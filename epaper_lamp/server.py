#!/bin/python3
from flask import Flask,render_template,request
from onem2m import *
import os
import logging

import subprocess

logg = logging.getLogger(__name__)

app = Flask(__name__,
            static_url_path='', 
            static_folder='./static',
            template_folder='./templates')


@app.route("/say",methods=['POST'])
def handle_speech():
    content_type = request.headers.get("Content-Type")
    if(content_type == 'application/json'):
        json = request.json
        text=json['text']
        language=json['language']
        subprocess.run(['google_speech','-l',language,f"'{text}'"])
        logg.debug("handling server speech")
        return "Playing Audio"

@app.route("/playmusic",methods=["POST"])
def handle_music():
    content_type = request.headers.get("Content-Type")
    if(content_type == "application/json"):
        json=request.json
        filename = json['file']
        logg.debug("handling requested music file")
        subprocess.run(['ffplay',filename,'-nodisp'])
        return "Playing Music"


@app.route("/")
def loadserver():
    aqi_node = AirQuality("AE-AQ","AQ-AD95-00").getData()
    solar_node = SolarNode("AE-SL","SL-VN03-00").getData()
    water_node = WaterQuality("AE-WM/WM-WD","WM-WD-PH02-00").getData()
    water_flow = WaterFlow("AE-WM/WM-WF","WM-WF-PH03-02").getData()
    #logg.debug("handling speech now")
    #thanksfortedtalk = "Welcome to Smart Pole, The Current temperature is " + str(round(aqi_node['temp'])) + " degree Centigrade , with Relative Humidity of " + str(round(aqi_node['rH'])) + "%, The current Air Quality is " + str(round(aqi_node['AQI']))
    #subprocess.run(['google_speech','-l','en-ca',thanksfortedtalk])
    return render_template(
        "index.html",
            AIRQ = {
                "emoji":"☁",
                "temp":round(aqi_node["temp"]),
                "AQI":round(aqi_node["AQI"]),
                "hum":int(aqi_node["rH"])
            },
            NODES=[
                {
                    "NAME":"Solar Power Generated",
                    "LOC":"VINDHYA",
                    "DATA":solar_node["energy"],
                    "UNIT":"kwh"
                },
                {
                    "NAME":"Water Quality - TDS",
                    "LOC":"PUMP HOUSE 03",
                    "DATA":water_node["Compensated_TDS_value"],
                    "UNIT":"ppm"
                },
                {
                    "NAME":"Water Flow Measured",
                    "LOC":"PUMP HOUSE 02",
                    "DATA":water_flow["Total_Flow"],
                    "UNIT":"m^3"
                }
            ],
            IMAGES={
                "iiith_logo":"https://upload.wikimedia.org/wikipedia/en/e/e1/International_Institute_of_Information_Technology%2C_Hyderabad_logo.png",
                "scrc_logo":"https://i.imgur.com/okNJq1H.png",
                "wisun_logo":"https://www.st.com/content/dam/category-pages/wireless-connectivity/logos/wisun-logo.png",
                "main_map":"https://i.imgur.com/ErhKofl.png"
            }
    )

def runserver(ip,port):
    app.run(ip,port)
    

logg.debug("Flask Server running on " + str(os.getpid()))

if(__name__ == "__main__"):
    app.run("0.0.0.0","8000")
