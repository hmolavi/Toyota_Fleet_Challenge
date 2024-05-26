#Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import rclpy
import numpy as np
import math

#Start ros with initializing the rclpy object
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = True
if not TMMC_Wrapper.is_SIM:
    #Specify hardware api
    TMMC_Wrapper.use_hardware()
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#Debug messaging 
print("running main")

#start processes
#add starter functions here

robot.start_keyboard_control()   #this one is just pure keyboard control

#rclpy,spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

#consts
#area coverage by lidar in a range of 20 degrees. In Rad
MinDist = 0.4
LOfRobotAngle1 = 1.92
LOfRobotAngle2 = 1.39
FOfRobotAngle1 = 0.18
FOfRobotAngle2 = -0.18
#run control functions on loop
try:
    print("Entering the robot loop which cycles until the srcipt is stopped")
    while True:

        #rclpy,spin_once is a function that updates the ros topics once
        rclpy.spin_once(robot, time_out=0.1)
        lidar_data_mesg = robot.checkScan()
        #robot.send_cmd_vel(0.2,0.0)
        
        #Add looping functionality here
        #detects if object is to the left
        if(robot.autnomis == True):
            robot.send_cmd_vel(0.2,0.0)
            if robot.lidar_data_too_close(lidar_data_mesg, FOfRobotAngle1,FOfRobotAngle2, MinDist) >= 0.8:
                print("object infront. turning Left")
                robot.rotate(90,1)

            
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")

finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()
