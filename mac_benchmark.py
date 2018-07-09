import cmx
import sh
import json
import argparse
import time
import socket

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
    for i in range(n):
        airport("-s") # force rescan
        print(cmx.locate_ip(ip, config))