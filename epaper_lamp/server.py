from flask import Flask,render_template
from onem2m import *
app = Flask(__name__,
            static_url_path='', 
            static_folder='./static',
            template_folder='./templates')

@app.route("/")
def loadserver():
    aqi_node = AirQuality("AE-AQ","AQ-FG00-00").getData()
    solar_node = SolarNode("AE-SL","SL-VN03-00").getData()
    water_node = WaterQuality("AE-WM/WM-WD","WM-WD-PH02-00").getData()
    water_flow = WaterFlow("AE-WM/WM-WF","WM-WF-PH03-02").getData()

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
                    "NAME":"Solar Power",
                    "LOC":"VINDHYA",
                    "DATA":solar_node["energy"],
                    "UNIT":"kwh"
                },
                {
                    "NAME":"Water Quality",
                    "LOC":"PUMP HOUSE 03",
                    "DATA":water_node["Compensated_TDS_value"],
                    "UNIT":"ppm"
                },
                {
                    "NAME":"Water Flow",
                    "LOC":"PUMP HOUSE 02",
                    "DATA":water_flow["Total_Flow"],
                    "UNIT":"m^3"
                }
            ]
    )


if(__name__ == "__main__"):
    app.run()