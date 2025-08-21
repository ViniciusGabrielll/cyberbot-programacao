# bibliotecas

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
Drive = DriveBase(motorDir, motorEsq, wheel_diameter=30 ,axle_track=150)

sensorDir = ColorSensor(Port.C)
sensorEsq = ColorSensor(Port.F)

ultrasonico = UltrasonicSensor(Port.E)
ultrasonicoLado = UltrasonicSensor(Port.D)
Color.WHITE = Color(193, 11, 90) 
Color.GREEN = Color(h=183, s=50, v=24)
Color.BLACK = Color(200, 15, 22) 
Color.GRAY = Color(195, 31, 17)
Color.RED = Color(351, 91, 67) 
Color.PRATA = Color(h=200, s=20, v=52)
Color.PRATAFALSO = Color(h=195, s=7, v=57)
myColors = (Color.GREEN, Color.WHITE, Color.BLACK, Color.GRAY, Color.RED, Color.PRATA, Color.PRATAFALSO)
sensorDir.detectable_colors(myColors)
sensorEsq.detectable_colors(myColors)


while True: 
    print("Direito: ", sensorDir.hsv())
    print("Color: ", sensorDir.color())
    print("Reflect: ", sensorDir.reflection())
    print("-----------------")
    print("Esquerdo: ", sensorEsq.hsv())
    print("Color: ", sensorEsq.color())
    print("Reflect: ", sensorEsq.reflection())
    print("-----------------")
    print("Ultrasonica Lado: ", ultrasonicoLado.distance())
    wait(500)

    # branco = esq:65/69   dir:66/71
    # verde = esq:18/19   dir:15/16
    # preto = esq:19/20   dir:21/22