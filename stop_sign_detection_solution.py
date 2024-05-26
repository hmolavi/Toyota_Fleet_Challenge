# Start with imports, ie: import the wrapper
# import other libraries as needed
import TMMC_Wrapper
import rclpy
import numpy as np
import math
from ultralytics import YOLO

# Start ros with initializing the rclpy object
if not rclpy.ok():
    rclpy.init()

# Simulation Mode
TMMC_Wrapper.is_SIM = False

if not TMMC_Wrapper.is_SIM:
    TMMC_Wrapper.use_hardware()

if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

# Debug messaging
print("running main")

# YOLO model
model = YOLO('yolov8n.pt')

# State variables
stop_sign_detected = False

# start processes
# Used for manual overrides
robot.start_keyboard_control()   #this one is just pure keyboard control

# rclpy.spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

# Run control functions on loop
try:
    print("Entering the robot loop which cycles until the script is stopped")
    
    while True:
        # rclpy.spin_once is a function that updates the ros topics once
        rclpy.spin_once(robot, timeout_sec=0.1)
    
        robot.checkImageRelease()

        # Add looping functionality here
        img_msg = robot.checkImage()
        if img_msg:
            img = robot.rosImg_to_cv2()
            stop_sign_detected, x1, y1, x2, y2 = robot.ML_predict_stop_sign(model, img)
            if stop_sign_detected:
                print("Stop sign detected! Stopping the robot.")
                stop_sign_detected = False

except KeyboardInterrupt:
    print("Keyboard interrupt received. Stopping...")

finally:
    # When exiting program, run the kill processes
    # Add functionality to ending processes here
    robot.destroy_node()
    rclpy.shutdown()
