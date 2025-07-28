from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# definir

hub = InventorHub(broadcast_channel=1)
ooteck2 = InventorHub(observe_channels=[2])

motorDir = Motor(Port.A)
motorEsq = Motor(Port.B, Direction.COUNTERCLOCKWISE)
Drive = DriveBase(motorDir, motorEsq, wheel_diameter=30, axle_track=150)

sensorDir = ColorSensor(Port.D)
sensorEsq = ColorSensor(Port.C)

ultrasonico = UltrasonicSensor(Port.E)
ultrasonicoLado = UltrasonicSensor(Port.F)
Color.WHITE = Color(193, 11, 90) 
Color.GREEN = Color(191, 57, 22)
Color.BLACK = Color(215, 17, 80) 
Color.GRAY = Color(195, 31, 17)
Color.RED = Color(351, 91, 67) 
Prata = Color(206, 24, 78)
myColors = (Color.GREEN, Color.WHITE, Color.BLACK, Color.GRAY, Color.RED, Prata)
sensorDir.detectable_colors(myColors)
sensorEsq.detectable_colors(myColors)

cronometro = StopWatch()

def girarGraus(graus, velocidade):
    hub.imu.reset_heading(0)
    if graus > 0:
        while(hub.imu.heading() >= graus * -1):
            motorDir.dc(velocidade)
            motorEsq.dc(-velocidade)
    else:
        while(hub.imu.heading() <= graus * -1):
            motorDir.dc(-velocidade)
            motorEsq.dc(velocidade)

def andar():
    motorDir.dc(100)
    motorEsq.dc(100)

ehAEntradaDoResgate = True
while True:
    andar()
    if(ultrasonicoLado.distance() < 100 and ehAEntradaDoResgate == True):
        Drive.straight(40)
        Drive.stop()
        wait(50)
        if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
            Drive.stop()
            wait(10000000)
            print("Resgate")
        else:
            Drive.straight(-40)
            ehAEntradaDoResgate = False
            cronometro.reset()

    if not ehAEntradaDoResgate and cronometro.time() >= 3000:
        ehAEntradaDoResgate = True