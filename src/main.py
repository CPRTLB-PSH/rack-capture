import threading
from picamWrapper import take_image
import util

config_data = util.get_config()


# Set up capture loop
capture_timer = threading.Timer(util.string_to_seconds(config_data.interval))



take_image("/home/icyy/testimg.jpg")
