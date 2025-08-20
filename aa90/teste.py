from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

ooteck2 = InventorHub(broadcast_channel=2)
hub = InventorHub(observe_channels=[1])

garra = Motor(Port.D)
compartimento = Motor(Port.B)

backColorSensor = ColorSensor(Port.A)
frontColorSensor = ColorSensor(Port.E)

Color.RED = Color(350, 84, 27)
Color.GREEN = Color(182, 86, 32)
Color.WHITE = Color(180, 5, 19)
Color.NONE = Color(0, 0, 0)
myColors = (Color.GREEN, Color.WHITE, Color.RED, Color.NONE)
backColorSensor.detectable_colors(myColors)
frontColorSensor.detectable_colors(myColors)

garra.run_time(-1000, 1000)
wait(1000)
garra.run_time(1000, 1000)