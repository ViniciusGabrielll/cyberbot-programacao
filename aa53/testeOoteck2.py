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

corDir = sensorDir.color()
corEsq = sensorEsq.color()

veloPadrao = 100

saida = False

ultrasonico.lights.on()
ultrasonicoLado.lights.on()



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

def prataOuPreto():
    print("PRETO OU PRATA")
    Drive.stop()
    wait(500)
    if(sensorDir.color() == Prata or sensorEsq.color() == Prata):
        prata()
    elif(sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK):
        preto()

def saidaAoLado():
    Drive.straight(10)
    Drive.stop()
    wait(100)
    if ultrasonicoLado.distance() >= 1900:
        while ultrasonico.distance() <= 1900:
            print("GIRANDO PARA SAIDA")
            motorDir.dc(veloPadrao)
            motorEsq.dc(-veloPadrao)
        while corDir != Color.WHITE:
            motorDir.dc(20)
            motorEsq.dc(20)
        Drive.stop()

def prata():
    print("PRATA")
    Drive.straight(10)
    Drive.straight(-50)
    girarGraus(-90, veloPadrao)
    Drive.straight(250)

def preto():
    global saida
    print("VIU PRETO!!!")
    saida = True

def andar():
    if ultrasonico.distance() <= 100:
        motorDir.dc(-veloPadrao)
        motorEsq.dc(-50)
        while ultrasonico.distance() <= 50:
            motorDir.dc(veloPadrao)
            motorEsq.dc(-veloPadrao)
        wait(500)
    else:
        motorDir.dc(veloPadrao)
        motorEsq.dc(veloPadrao)

while not saida:
    andar()
    if(sensorDir.color() != Color.WHITE or sensorEsq.color() != Color.WHITE):
        prataOuPreto()
    if(ultrasonicoLado.distance() >= 1900):
        saidaAoLado()