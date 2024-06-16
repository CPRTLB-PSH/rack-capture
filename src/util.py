import sys
import os
import json

CONFIG_PATH = os.environ["CONFIG_PATH"] if "CONFIG_PATH" in os.environ else "./config.json"
config_data = None
try:
    with open(CONFIG_PATH, "r") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError as e:
    print("⚠️ Could not read config file from CONFIG_PATH: "+CONFIG_PATH)
    sys.exit()

def get_config():
    return config_data

def string_to_seconds(string: str): #type hints pls
    return 300