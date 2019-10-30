from dronekit import connect, VehicleMode
import sys
from rplidar import RPLidar
import time
import math

# Connect to Mission Planner SITL
vehicle = connect("/dev/ttyACM0",wait_ready=True)
#vehicle = connect("10.10.2.163:14553",wait_ready=True)
#vehicle = connect("192.168.0.109:14552",wait_ready=True)

# Defining distance sensor mavlink message generation function
def sensor_data(d,o):
    msg=vehicle.message_factory.distance_sensor_encode(
        0,
        5,
        1000,
        d,
        0,
        1,
        o,
        0,
        )
    vehicle.send_mavlink(msg)
    
# Defining distance sensor data classification
def orientation(a):    
    global o
    if (0<= a and a< 22.5):
        o = 0

    elif (22.5<= a and a<67.5):
        o = 1

    elif (67.5<= a and a< 112.5):
        o = 2

    elif (112.5<= a and a<157.5):
        o = 3

    elif (157.5<= a and a<202.5):
        o = 4

    elif (202.5<= a and a< 247.5):
        o = 5

    elif (247.5<= a and a<292.5):
        o = 6

    elif (292.5<= a and a<337.5):
        o = 7
        
    elif (337.5<=a and a<360):
        o = 0
    return (o)

# Defining connect to lidar function
def connect():
    global lidar
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    lidar.clear_input()
    health = lidar.get_health()
    print(health)

# Defining obstacle avoidance function
def Avoidance():
    i=0
    for measurement in lidar.iter_measurments(max_buf_meas=80):
        a = measurement[2]
        dRaw = (measurement[3])/10
        d = round(dRaw)
        # Cal orientation
        o = int(orientation(a))
        
        if (d>=200):
            i+=1
            print('ok'+str(i))
            sensor_data(int(d),o)
        elif (30<d<200):
            print(d)
            lidar.stop()
            lidar.stop_motor()
            lidar.reset()
            lidar.disconnect()
            break

# Defining function after break
def Waiting():
    x=o
    for x in range (30):
        if vehicle.mode.name == "BRAKE":
            time.sleep(1)
        else:
            time.sleep(1)
            break
    if vehicle.mode.name == "BRAKE":
        print("No pilot response, A/C initiates RTL")
        print("Mode: %s" % vehicle.mode.name)
        vehicle.mode = VehicleMode('RTL')
        time.sleep(5)
    
# Wait for arming

while not vehicle.armed:      
    print(" Waiting for arming...")
    time.sleep(1)

print('Vehicle armed, initialising obstacle avoidance in 10s')
time.sleep(5)

# Function

while 1:  
    if vehicle.mode.name =='LAND':
        print('Landing mode engaged, Obstacle avoidance disabled')
        break
    connect()
    time.sleep(5)
    Avoidance()   
    if vehicle.mode.name =='LAND':
        print('Landing mode engaged, Obstacle avoidance disabled')
        break
    vehicle.mode = VehicleMode("BRAKE")
    time.sleep(1)
    print("Obstacle detected!, Flight mode forced: %s" % vehicle.mode.name)
    Waiting()

