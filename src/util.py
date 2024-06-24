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

def get_env(env_name: str) -> str:
    """
    Act as a wrapper for getting environment variables. Uses default values if nothing is set
    """
    if os.environ[env_name]:
        return os.environ[env_name]
    else:
        if env_name == "UPLOAD_DIR":
            return "./data/uploads"
        elif env_name == "CACHE_DIR":
            return "./data"
        elif env_name == "CONFIG_PATH":
            return "./config.json"


def string_to_seconds(string: str) -> int:
    """
    Takes in a string, like "3d", or "40h", and turns it into seconds
    m = minutes, h = hours, d = days, "w" = weeks
    """
    unit = string[-1]
    quantity = int(string[:-1])
    if unit == "s":
        return quantity
    if unit == "m":
        return quantity * 60
    elif unit == "h":
        return quantity * 60 * 60
    elif unit == "d":
        return quantity * 60 * 60 * 24
    elif unit == "w":
        return quantity * 60 * 60 * 24 * 7
    else:
        raise ValueError(f"string_to_seconds(): {string} is not in the correct format")
