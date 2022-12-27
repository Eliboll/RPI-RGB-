from urllib import request
from flask import Flask, request
import rgb

app = Flask(__name__)

rgb = rgb.rgb(24)

@app.route("/", methods=['GET'])
def hello_world():
    args = request.args
    passed_value = (args.has_key("r") and args.has_key("g") and args.has_key("b") ) or args.has_key("hex")

@app.route("/rotate")
def rotate():
    rgb.full_rotate()
    return "200 OK"

@app.route("/rainbow_cycle")
def rainbow_cycle():
    rgb.rainbow_cycle()
    return "200 OK"

@app.route("/stop")
def stop():
    rgb.set_stop()
    return "200 OK"

@app.route("/off")
def off():
    rgb.fill((0,0,0))
    return "200 OK"

@app.route("/uniqlo", methods=['GET'])
def uniqlo():
    args = request.args

    buffer = 5
    if "buffer" in args:
        buffer = int(args['length'])
    length = 3
    if "length" in args:
        length = int(args["length"])

    passed_value = ("r" in args and "g" in args and "b" in args ) or "hex" in args
    if passed_value:
        if "hex" in args:
            val = hex_to_touple(args["hex"])
        else:
            val = (int(args["r"]),int(args["g"]),int(args["b"]))
        rgb.uniqlo(rgb=val,buffer=buffer,length=length)
    else:
        rgb.uniqlo(buffer=buffer,length=length)
    return "200 OK"


def hex_to_touple(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
