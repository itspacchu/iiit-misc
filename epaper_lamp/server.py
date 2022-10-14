#!/bin/python3
from flask import Flask,render_template,request
from onem2m import *
import os
import logging
from processing import computeIntensity
import subprocess

# from soundmeter import sound_dB # Broken cutils

SCALE_LUX = 9
DC_LUX = 8

logg = logging.getLogger(__name__)

app = Flask(__name__,
            static_url_path='', 
            static_folder='./static',
            template_folder='./templates')




def handle_sounddb():
    os.seteuid(65534)
    dB = 0
    with open("./soundv","rb") as sval:
        dB = sval.readline().decode("utf-8")
    ret = ""
    for i in dB:
        if(i.isalnum()):
            ret+=i
    print(ret)
    return ret

@app.route("/getsay",methods=["GET"])
def handle_unsecure_speech():
    text = request.args['text']
    subprocess.run(['sudo','google_speech','-l',"en-ca",f"'{text}'"])
    return "Success"

@app.route("/say",methods=['POST'])
def handle_speech():
    content_type = request.headers.get("Content-Type")
    if(content_type == 'application/json'):
        json = request.json
        text=json['text']
        language=json['language']
        subprocess.run(['sudo','google_speech','-l',language,f"'{text}'"])
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
    sound_intensity = handle_sounddb()
    rain_check = "Today there might be a high chance of rain" if(int(aqi_node["rH"]) > 70 and round(aqi_node["temp"]) < 30) else "Today there is very low chance of rain"
    logg.debug("handling speech now")
    thanksfortedtalk = "Welcome to Smart Pole, The Current temperature is " + str(round(aqi_node['temp'])) + " degree Centigrade , with Relative Humidity of " + str(round(aqi_node['rH'])) + "%, The current Air Quality is " + str(round(aqi_node["AQI"]) + "," + raincheck
    subprocess.run(['sudo','google_speech','-l','en-ca',thanksfortedtalk])

    lux = computeIntensity("./frames/capture.jpg")/SCALE_LUX + DC_LUX

    return render_template(
        "index.html",
            PACCHU = {
                "dB":handle_sounddb(),
                "lux":round(lux,0),
            },
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
                "main_map":"https://i.imgur.com/ErhKofl.png",
		"wisun_map":"https://i.imgur.com/E8EefRZ.png"
            }
    )

# @app.route("/w")
# def loadwisun():
#     aqi_node = AirQuality("AE-AQ","AQ-AD95-00").getData()
#     solar_node = SolarNode("AE-SL","SL-VN03-00").getData()
#     water_node = WaterQuality("AE-WM/WM-WD","WM-WD-PH02-00").getData()
#     water_flow = WaterFlow("AE-WM/WM-WF","WM-WF-PH03-02").getData()
#     sound_intensity = handle_sounddb()
#     lux = computeIntensity("./frames/capture.jpg")/SCALE_LUX + DC_LUX
#     #logg.debug("handling speech now")
#     #thanksfortedtalk = "Welcome to Smart Pole, The Current temperature is " + str(round(aqi_node['temp'])) + " degree Centigrade , with Relative Humidity of " + str(round(aqi_node['rH'])) + "%, The current Air Quality is " + str(round(a>
#     #subprocess.run(['google_speech','-l','en-ca',thanksfortedtalk])
#     return render_template(
#         "wisun.html",
#             PACCHU = {
#                 "dB":handle_sounddb(),
#                 "lux":round(lux,0),
#             },
#             AIRQ = {
#                 "emoji":"   ^x^a",
#                 "temp":round(aqi_node["temp"]),
#                 "AQI":round(aqi_node["AQI"]),
#                 "hum":int(aqi_node["rH"])
#             },
#             NODES=[
#                 {
#                     "NAME":"Wisun Nodes",
#                     "LOC":"VINDHYA",
#                     "DATA":30,
#                     "UNIT":"Active"
#                 },
#                 {
#                     "NAME":"Alive",
#                     "LOC":"PUMP HOUSE 03",
#                     "DATA":13,
#                     "UNIT":"Nodes"
#                 },
#                 {
#                     "NAME":"Inactive",
#                     "LOC":"PUMP HOUSE 02",
#                     "DATA":17,
#                     "UNIT":"Nodes"
#                 }
#             ],
#             IMAGES={
#                 "iiith_logo":"https://upload.wikimedia.org/wikipedia/en/e/e1/International_Institute_of_Information_Technology%2C_Hyderabad_logo.png",
#                 "scrc_logo":"https://i.imgur.com/okNJq1H.png",
# 		"wisun_logo":"https://news.silabs.com/image/silicon-labs-black-2014-275x200px_newsroom-logo-page2.png",
#                 "main_map":"https://i.imgur.com/ErhKofl.png",
#                 "wisun_map":"https://i.imgur.com/0sTxR3e.png"
#             }
#     )

def runserver(ip,port):
    app.run(ip,port)

logg.debug("Flask Server running on " + str(os.getpid()))

if(__name__ == "__main__"):
    print("Consider not running the server as standalone please run ./paco.py")
    app.run("0.0.0.0","42069")
