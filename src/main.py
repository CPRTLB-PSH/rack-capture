import sched
import os
import sys
import time
import datetime
import json
from picamWrapper import take_image
import util

LOGIC_INTERVAL = 1 # How often to run do_snapshot_logic()
UPLOAD_DIR = os.environ["UPLOAD_DIR"] if "UPLOAD_DIR" in os.environ else "./data"

scheduler = sched.scheduler()
config_data = util.get_config()
batch_num_formatted = '{:04d}'.format(config_data['batch_num'])
dataset_path = os.path.join(util.get_env("UPLOAD_DIR"), config_data["dataset_name"], f"batch-{batch_num_formatted}")

def do_snapshot_logic():
    global timer
    metadata_file_path = os.path.join(dataset_path, "metadata.json")
    metadata = None

    with open(metadata_file_path, "r") as metadata_file:
        metadata = json.load(metadata_file)

    # Check if collection time is over
    if time.time() > metadata["start_tick"] + util.string_to_seconds(config_data["period"]):
        print("Dataset collection is done, exiting...")
        sys.exit()
    
    # Check if it's time to take another snapshot
    if time.time() < metadata["last_capture"] + util.string_to_seconds(config_data["img_interval"]):
        return
    
    # Take the snapshot
    next_num = "{:05d}".format(metadata["num_captures"] + 1)
    try:
        take_image(os.path.join(dataset_path, f"{next_num}.jpg"))
    except Exception as e:
        print(f"error taking image #{next_num}:")
        print(e)
    
    metadata["num_captures"] += 1
    metadata["last_capture"] = time.time()

    # Write latest stats
    with open(metadata_file_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


    


def main():
    # Set up dataset directory if not already set up
    if not os.path.exists(os.path.join(dataset_path, "metadata.json")):
        print("Creating metadata file...")
        os.makedirs(dataset_path, exist_ok=True)
        metadata = {
            "start_tick": int(time.time()),
            "start_tick_readable": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_capture": 0,
            "num_captures": 0
        }
        print(os.path.join(dataset_path, "metadata.json"))
        with open(os.path.join(dataset_path, "metadata.json"), "w") as file:
            json.dump(metadata, file) 
            print(f"Created metadata.json at {dataset_path}")
           

    # Begin capture loop
    print("Starting capture loop!")
    while True:
        do_snapshot_logic()
        time.sleep(LOGIC_INTERVAL)


if __name__ == "__main__":
    main()

