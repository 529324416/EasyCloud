'''
config module
this script will read base config and save to a Dict Object
'''


import json

CONFIG_PATH = "./config/baseconfig.cfg"

with open(CONFIG_PATH,"r",encoding='utf-8') as f:
    config = json.load(f)