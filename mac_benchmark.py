import cmx
import sh
import json
import argparse
import time
import socket
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
import sys

if __name__ == "__main__":
    with open("config.json") as config_file:
        config = json.load(config_file)
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", default=10, type=int, help="number of times to locate")
    args = parser.parse_args()
    n = args.n
    ip = socket.gethostbyname(socket.gethostname())
    out = []
    start = time.time()
    airport = sh.Command("airport")
    
    data = cmx.locate_ip(ip, config)
    floor_map = requests.get("{}{}".format(config["map_endpoint"], data["response"]["mapInfo"]["image"]["imageName"]), headers={"Authorization" : cmx.basic(config["username"], config["password"])})
    img = Image.open(BytesIO(floor_map.content))
    draw = ImageDraw.Draw(img)
    for i in range(n):
        sys.stdout.write("\r{}/{}".format(i+1, n))
        sys.stdout.flush()
        airport("-s") # force rescan
        current = cmx.locate_ip(ip, config)
        cmx.draw_position(draw, current)
    
    print("\ndone! showing image")
    img.show()
