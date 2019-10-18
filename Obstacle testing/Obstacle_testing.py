from dronekit import connect, VehicleMode
import random
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
global d
global d1
# Make continuous
while vehicle.mode.name !=('LAND'or'RTL'):
    print("Mode: %s" % vehicle.mode.name)
# Simulate Obstacle avoidance
# Random reading generator
    i=1
    try:
        d = random.randint(10,1000)
        d1 = random.randint(10,1000)
        print(d)
        print(d1)
        if d>=20 and d1>=20:
            i+=1
            print('ok'+str(i))
            sensor_data(d,0)
            sensor_data(d1,4) 
            time.sleep(0.1)
        else:
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
    except vehicle.mode.name =='LAND':
        break
    break
