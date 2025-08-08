from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()

sensorDir = ColorSensor(Port.D)
sensorEsq = ColorSensor(Port.C)

Color.WHITE = Color(193, 11, 90) 
Color.GREEN = Color(h=180, s=51, v=27)
Color.BLACK = Color(200, 15, 22) 
Color.GRAY = Color(195, 31, 17)
Color.RED = Color(351, 91, 67) 
WHITEANDGREEN = Color(h=185, s=55, v=26)
Prata = Color(206, 24, 78)
myColors = (Color.GREEN, Color.WHITE, Color.BLACK, Color.GRAY, Color.RED, Prata)
sensorDir.detectable_colors(myColors)
sensorEsq.detectable_colors(myColors)
i = 0
while True: 
    print("Direito: ", sensorDir.hsv())
    print("Color: ", sensorDir.color())
    print("Reflect: ", sensorDir.reflection())
    print("-----------------")
    print("Esquerdo: ", sensorEsq.hsv())
    print("Color: ", sensorEsq.color())
    print("Reflect: ", sensorEsq.reflection())
    print("-----------------")
    wait(500)

    # branco = esq:65/69   dir:66/71
    # verde = esq:18/19   dir:15/16
    # preto = esq:19/20   dir:21/22