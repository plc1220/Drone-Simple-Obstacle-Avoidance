from dronekit import connect, VehicleMode, LocationGlobal
import sys
from rplidar import RPLidar
import time
import math

# Connect to Mission Planner SITL
vehicle = connect('127.0.0.1:14551',wait_ready=True)

# Defining home location
def home():
    current_location = vehicle.location.global_frame
    vehicle.home_location = current_location
    print("New Home Location: %s" % vehicle.home_location)

    # Confirm current value on vehicle
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    print("Check new home location: %s" % vehicle.home_location)

    return None

# Defining distance finder
def dist(Location1, Location2):
    dlat = Location1.lat - Location2.lat
    dlon = Location2.lon - Location2.lon
    distance = math.sqrt((dlat * dlat) + (dlon * dlon)) * 1.113195e5
    return distance

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
    print (msg)
    
# Defining distance sensor data classification
def orientation(a):
    global o
    if (0<= a and a<= 45):
          o = 0
    elif (46<= a and a<=90):
         o = 1
    elif (91<= a and a<= 135):
          o = 2            
    elif (136<= a and a<=180):
            o = 3  
    elif (181<= a and a<=225):
        o = 4
    elif (226<= a and a<= 270):
         o = 5
    elif (271<= a and a<=315):
        o = 6
    elif (316<= a and a<=359):
         o = 7
    return o

# Defining connect to lidar function
def connect():
    global lidar
    PORT_NAME = 'COM3'
    lidar = RPLidar(PORT_NAME)
    health = lidar.get_health()
    print(health)

# Defining obstacle avoidance function
def Avoidance():
    i=0
    for measurement in lidar.iter_measurments(max_buf_meas=80):
        a = measurement[2]
        dRaw = (measurement[3])/10
        d = round(dRaw)
        print(d)
        print(a)
        # Cal orientation
        o = int(orientation(a))
        print(o)
        
        if (d>=20):
            i+=1
            print('ok'+str(i))
            sensor_data(int(d),o)
        elif (0<d<20):
            lidar.stop()
            lidar.stop_motor()
            lidar.reset()
            lidar.disconnect()
            break

# Set home
home()

while not vehicle.armed:      
    print(" Waiting for arming...")
    time.sleep(1)

print('Vehicle armed, initialising obstacle avoidance in 30s')
time.sleep(30)

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
    time.sleep(30)
    while 1:
        if vehicle.mode.name == 'BRAKE':
            print("No pilot response, A/C initiates RTL")
            print("Mode: %s" % vehicle.mode.name)
            vehicle.mode = VehicleMode('RTL')
            time.sleep(5)
            break
        else:
            break
