from dronekit import connect, VehicleMode
import sys
from rplidar import RPLidar
import time


# Connect to Mission Planner SITL
vehicle = connect('127.0.0.1:14551',wait_ready=True)

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

# Connect to lidar
PORT_NAME = 'COM3'
lidar = RPLidar(PORT_NAME)
health = lidar.get_health()
print(health)

# Make continuous
while vehicle.mode.name !=('LAND'or'RTL'):
    print("Mode: %s" % vehicle.mode.name)
# Simulate Obstacle avoidance
    i=0
    for measurement in lidar.iter_measurments(max_buf_meas=500):
        a = measurement[2]
        dRaw = (measurement[3])/10
        d = round(dRaw)
        print(dRaw)
        print(d)
        print(a)

        o = int(orientation(a))
        print(o)
        if (d>=20):
            i+=1
            print('ok'+str(i))
            sensor_data(int(d),o)
        elif (0<d<20):
# Override RC, Channel 5(Flight Mode)
##print('set Flight Mode to RTL')
##t_end = time.time() + 60 * 5
##while time.time() < t_end:
##    vehicle.channels.overrides['5'] = 1685

# Swtich Flight mode to 'Brake'
            vehicle.mode = VehicleMode("BRAKE")
            print("Obstacle detected!, Flight mode forced: %s" % vehicle.mode.name)
            time.sleep(10)
        if vehicle.mode.name == 'BRAKE':
            print("No pilot response, A/C initiates RTL")
            print("Mode: %s" % vehicle.mode.name)
            vehicle.mode = VehicleMode('RTL')
            time.sleep(10)
        if vehicle.mode.name =='LAND':
            print('Landing Mode, obstacle avoidance diabled')
            lidar.stop()
            lidar.disconnect()
            break
    break
