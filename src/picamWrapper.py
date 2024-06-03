import time

# Conditional import of picam, for developing on systems that aren't a raspberry pi
picam = None
try:
    from picamera2 import Picamera2, Preview
    picam = Picamera2()
    picam.start_preview(Preview.NULL)
except:
    picam = None
    print("⚠️  Picamera2 was not loaded because it is not installed, and no images will be created on this system!") 
    print("⚠️  This is expected if you're running this NOT on a raspberry pi") 


def take_image(path: str):
    if not picam:
        print(f"Picam2 inactive: Image would have been placed in: {path}")
        return
    
    picam.start_and_capture_file(path)
    pass