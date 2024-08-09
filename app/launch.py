# Launch the app through this script to get a list of (working) cameras
from pygrabber.dshow_graph import FilterGraph
import cv2

def get_available_cameras():
    devices = FilterGraph().get_input_devices()
    available_cameras = {}
    
    for device_index, device_name in enumerate(devices):
        test_capture = cv2.VideoCapture(device_index)
        if test_capture.read()[0] is True:
            available_cameras[device_index] = device_name
        
        test_capture.release()
            
    return available_cameras

# Create a save file if it doesn't exist
file = open('camera_list.txt', 'a')
file.close()

# Open the save file to write on it
file = open('camera_list.txt', 'w')

#Get an list of available cameras
cameras = get_available_cameras()

for index in cameras:
    file.write(f'{index} // {cameras[index]}\n')
    
file.close()   

import main
main.YogaApp().run()

