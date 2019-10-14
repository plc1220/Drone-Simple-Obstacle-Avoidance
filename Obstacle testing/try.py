import sys
from rplidar import RPLidar
import time

PORT_NAME = 'COM3'

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
    
    return (o)

def record():
    lidar = RPLidar(PORT_NAME)

    health = lidar.get_health()
    print(health)
    
    try:
        for measurement in lidar.iter_measurments():
            print(measurement)
            a = measurement[2]
            o=orientation(a)

            print(o)
            
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    
if __name__ == '__main__':
    record()
