
from time import sleep
import requests,sys
from random import randint

USRNAME,PASSWD = "",""

IIIT_OM2M_URL_BASE = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/"
OM2M_HEADERS = {
    'X-M2M-Origin': '{USRNAME}:{PASSWD}',
    'Accept': 'application/json'
}

IIIT_WLED_URL = f"http://{sys.argv[1]}/"

def FETCH_URL(node_loc="AE-SR",node_name="SR-AQ",sub_grp="SR-AQ-KH95-00"):
    return f"{IIIT_OM2M_URL_BASE}{node_loc}/{node_name}/{sub_grp}/Data/la"


def fetch_data(url:str):
    return requests.get(FETCH_URL(), headers=OM2M_HEADERS).json()

def fetch_lab_stuff():
    raw_data = fetch_data(FETCH_URL)['m2m:cin']['con'][1:].split(",")
    data_dict = {}
    CO2,TEMP,REL_HUM = [float(i.replace("]","")) for i in raw_data[1:4]]
    return {
        "CO2":CO2,
        "TEMP":TEMP,
        "REL_HUM":REL_HUM
    }

def write_WLED_colors(C1,C2,C3,Brightness=255,speed=64,intensity=125,palette=4):
    """
    C1,C2,C3    : Sets Color 
    Brightness  : Sets Master brightness ( default 255 )
    Speed       : Sets Master speed control ( default 64 )
    Intensity   : Set Effect Intensity ( default 125 )
    Palette     : Set Pallete Index [ Starts with 0 ]  ( default 4 )
    """
    CMD = f"{IIIT_WLED_URL}win&A={Brightness}&SX={speed}&IX={intensity}&CL=H{C1}&C2=H{C2}&C3=H{C3}&FP={palette}"
    send = requests.get(CMD)
    if(send):
        return ">>> ACK"
    else:
        return ">>> NACK"

def R2X(R:int,G:int,B:int):
    """
    Converts R,G,B Values to HEX
    """
    return '%02x%02x%02x' % (int(R), int(G), int(B))

def remap(value,old_min,old_max,new_min,new_max):
    """
    Remap (value) ranging from (old_min to old_max) to (new_min to new_max)
    """
    return ((value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

def reColors(value,ColArr):
    if(value < 0.25):
        return ColArr[0]
    elif(value < 0.5):
        return ColArr[1]
    elif(value < 0.75):
        return ColArr[2]
    else:
        return ColArr[3]


if(__name__ == "__main__"):
    if('-h' in sys.argv):
        print("""
        ## fetches data from onem2m server and pushes to WLED
        onem2m_WLED.py <wled-ip> <username> <passwd> <sleep-time>

        wled-ip    : IP of WLED instance
        username   : Username of onem2m server
        passwd     : Password for onem2m server
        sleep-time : Sleep time between updating the WLED colors
        """)
        exit()
    if(len(sys.argv) != 5):
        print("All Args: <wled-ip> <username> <passwd> <sleep-time>")
        exit()

    USRNAME,PASSWD = sys.argv[2],sys.argv[3]
    while(True):
        print("Fetching values from onem2m\n")
        LabData = fetch_lab_stuff() 

        #-------------------------------------------
        #TODO Work on creating a yaml config file
        """
        Set Colors here
        Co2_COLS[4] -> LOW,LOW_MID,HIGH_MID,HIGH
        Temp_COLS[4] -> LOW,LOW_MID,HIGH_MID,HIGH
        """

        Co2_COLS = ['4E944F','83BD75','B4E197','E9EFC0']
        Temp_COLS = ['187498','36AE7C','F9D923','EB5353']

        #--------------------------------------------

        Co2_COLOR = reColors(remap(LabData['CO2'],10,50,0,1),Co2_COLS)
        TEMP_COLOR = reColors(remap(LabData['TEMP'],17,43,0,1),Temp_COLS)

        print('<<< CO2:0h'+Co2_COLOR+';TEMP:0h'+TEMP_COLOR)
        res = write_WLED_colors(Co2_COLOR,Temp_COLS,TEMP_COLOR)
        print(res)
        if(res != "NACK"):
            sleep(int(sys.argv[4]))
        else:
            sleep(1)