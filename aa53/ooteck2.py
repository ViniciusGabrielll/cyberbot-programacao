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

while True:    
    if hub.ble.observe(1) == "garraBaixo":
        garra.run_time(-1000, 1000)
        ooteck2.display.number(44)
    elif hub.ble.observe(1) == "garraCima":
        garra.run_time(1000, 500)
        ooteck2.display.number(33)
    elif hub.ble.observe(1) == "colorSensor":
        if(frontColorSensor.color() != Color.WHITE):
            ooteck2.ble.broadcast("soltar")
        else:
            ooteck2.ble.broadcast("none")
    elif hub.ble.observe(1) == "abrirCompartimento":
        compartimento.run_time(-500, 500)
        ooteck2.display.number(55)
    elif hub.ble.observe(1) == "fecharCompartimento":
        compartimento.run_time(500, 500)
        ooteck2.display.number(66)
    else:
        ooteck2.display.number(11)
