from ast import arg
from flask import Flask,request
from requests import get,post
from flask_cors import CORS,cross_origin

DISCORD_WEBHOOK = ""

OM2M_HEADERS = {
    'X-M2M-Origin': 'guest:guest',
    'Accept': 'application/json'
}

DEV_OM2M_HEADERS = {
    'X-M2M-Origin': 'devtest:devtest',
    'Accept': 'application/json'
}
app = Flask(__name__)
CORS(app)

@app.route("/dev/",defaults={'path':''})
@app.route("/dev/<path:path>")
@cross_origin()
def proxydev(path):
    args = request.args
    get_param_str = "?"
    for i in args.keys():
        get_param_str += f"{i}={args[i]}&"
    ret = get(url="https://dev-onem2m.iiit.ac.in/" + path + get_param_str,headers=DEV_OM2M_HEADERS)
    return ret.json()

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
@cross_origin()
def proxy(path):
    args = request.args
    get_param_str = "?"
    for i in args.keys():
        get_param_str += f"{i}={args[i]}&"
    ret = get(url="https://onem2m.iiit.ac.in/" + path + get_param_str,headers=OM2M_HEADERS)
    data = {
        "content" : f"**{request.environ['HTTP_X_FORWARDED_FOR']}** : requested data\n```{path + get_param_str}```",
        "avatar_url":"https://media.discordapp.net/attachments/1061243097876541471/1061243213429604352/Screenshot_from_2023-01-07_16-39-07.png",
        "username" : "rubyproxy"
    }
    try:
        post(DISCORD_WEBHOOK,json=data)
    except:
        print("Webhook unavailable")
    return ret.json()

if("__main__"==__name__):
    data = {
        "content" : "Connected to OneM2M Server",
        "avatar_url":"https://media.discordapp.net/attachments/1061243097876541471/1061243213429604352/Screenshot_from_2023-01-07_16-39-07.png",
        "username" : "rubyproxy"
    }
    try:
        post(DISCORD_WEBHOOK,json=data)
    except:
        print("discord not accepting webhooks")
    app.run("0.0.0.0",8123)
