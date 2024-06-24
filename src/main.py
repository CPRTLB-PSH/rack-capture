import threading
import os
import sys
import time
import datetime
import json
from picamWrapper import take_image
import util

UPLOAD_DIR = os.environ["UPLOAD_DIR"] if "UPLOAD_DIR" in os.environ else "./data"

config_data = util.get_config()
dataset_path = os.path.join(util.get_env("UPLOAD_DIR"), config_data["dataset_name"], config_data["batch_num"])

def do_snapshot_logic():
    metadata = None
    with open(os.path.join(dataset_path, "metadata.json")) as metadata_file:
        metadata = json.load(metadata_file)

    
    
    # Check if collection time is over
    if time.time() > metadata["start_tick"] + util.string_to_seconds(config_data["period"]):
        print("Dataset collection is done, exiting...")
        sys.exit()
    
    # Check if it's time to take another snapshot
    if time.time() < metadata["last_capture"] + util.string_to_seconds(config_data["inteval"]):
        return
    
    # Take the snapshot
    next_num = "{:05d}".format(metadata["num_captures"] + 1)
    take_image(os.path.join(dataset_path, f"")) # format file name
    


def main():
    # Set up dataset directory if not already set up
    if not os.path.exists(os.path.join(dataset_path, "metadata.json")):
        metadata = {
            "start_tick": int(time.time()),
            "start_tick_readable": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_capture": 0,
            "num_captures": 0
        }
        with open(os.path.join(dataset_path, "metadata.json"), "w") as file:
            json.dump(metadata, file) 
            print(f"Created metadata.json at {dataset_path}")
           

    # Begin capture loop
    capture_timer = threading.Timer(10, do_snapshot_logic)
    print("Capture loop ready!")


if __name__ == "__main__":
    main()

