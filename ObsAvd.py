from dronekit import connect, VehicleMode
from smbus import SMBus
from time import sleep

# Connect to Vehicle
#vehicle = connect("/dev/ttyACM0",wait_ready=True)
vehicle = connect("10.10.3.88:14553",wait_ready=True)
#vehicle = connect("192.168.0.109:14552",wait_ready=True)

# Defining sensor
i2cbus = SMBus(1)

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
    
# Defining sensor function
def sensor():
    while 1:
        i2cbus.write_byte(0x70, 0x51)
        sleep(0.12)
        val = i2cbus.read_word_data(0x70, 0xe1)
        d = ((val >> 8) & 0xff | (val << 7) & 0x7ff)
        
        if (d < 50):
            print(d)
            break
        else :
            sensor_data(int(d),0)

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
    sensor()   
    if vehicle.mode.name =='LAND':
        print('Landing mode engaged, Obstacle avoidance disabled')
        break
    vehicle.mode = VehicleMode("BRAKE")
    time.sleep(1)
    print("Obstacle detected!, Flight mode forced: %s" % vehicle.mode.name)
    Waiting()