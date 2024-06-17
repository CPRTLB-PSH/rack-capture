import threading
import os
from picamWrapper import take_image
import util

config_data = util.get_config()

def data_snapshot():
    path = os.path.join(util.get_env("UPLOAD_DIR"),)

# Set up capture loop
capture_timer = threading.Timer(util.string_to_seconds(config_data.interval), data_snapshot)



take_image("/home/icyy/testimg.jpg")
