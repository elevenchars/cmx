from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import requests
import base64
import json
import socket
from io import BytesIO
import datetime

def basic(u, p):
    return "Basic " + base64.b64encode(("{}:{}".format(u,p)).encode()).decode("utf-8")

def locate_ip(ip, config):
    # print(config["location_endpoint"] + ip)
    location_data = requests.get("{}{}".format(config["location_endpoint"], ip), headers={"Authorization" : basic(config["username"], config["password"])}).json()
    return location_data

def display_ip(ip, config):
    data = locate_ip(ip, config)
    floor_map = requests.get("{}{}".format(config["map_endpoint"], data["response"]["mapInfo"]["image"]["imageName"]), headers={"Authorization" : basic(config["username"], config["password"])})
    img = Image.open(BytesIO(floor_map.content))
    draw = ImageDraw.Draw(img)
    draw = draw_position(draw, data)
    f = ImageFont.truetype("Arial.ttf", 16)
    info = """Retrieved on {}
    IP Address: {}
    Location: {}
    Confidence: {}
    """.format(datetime.datetime.now().strftime("%c"), ip, data["response"]["mapInfo"]["mapHierarchy"], data["response"]["confidenceFactor"])
    draw.text((0,0), info, (0,0,0), font=f)
    img.show()

def draw_position(draw, data):
    w = data["response"]["mapInfo"]["image"]["width"]
    h = data["response"]["mapInfo"]["image"]["height"]
    x = data["response"]["mapCoordinate"]["x"] / data["response"]["mapInfo"]["floorDimension"]["width"] * w
    y = data["response"]["mapCoordinate"]["y"] / data["response"]["mapInfo"]["floorDimension"]["length"] * h
    x = round(x)
    y = round(y)
    conf = data["response"]["confidenceFactor"]
    conf_x = conf / data["response"]["mapInfo"]["floorDimension"]["width"] * w
    conf_y = conf / data["response"]["mapInfo"]["floorDimension"]["length"] * h
    conf_x = round(conf_x)
    conf_y = round(conf_y)
    draw.rectangle([(x-conf_x, y-conf_y), (x+conf_x, y+conf_y)], outline=(0, 0, 255))
    draw.ellipse([(x-5, y-5), (x+5, y+5)], fill=(0, 255, 255))    
    return draw

if __name__ == "__main__":
    with open("config.json") as config_file:
        config = json.load(config_file)

    ip = socket.gethostbyname(socket.gethostname())
    display_ip(ip, config)