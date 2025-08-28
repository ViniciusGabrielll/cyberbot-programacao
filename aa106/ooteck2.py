from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

ooteck2 = InventorHub(broadcast_channel=2)
hub = InventorHub(observe_channels=[1])

garra = Motor(Port.B)
compartimento = Motor(Port.D)

frontColorSensor = ColorSensor(Port.F)

Color.WHITE = Color(193, 11, 90) 
Color.GREEN = Color(h=183, s=87, v=57)
Color.BLACK = Color(200, 15, 22) 
Color.GRAY = Color(195, 31, 17)
Color.RED = Color(351, 91, 67) 
Color.LONGE = Color(h=204, s=19, v=32)
Color.MAISLONGE = Color(h=180, s=20, v=13)
Color.NONE = Color(0, 0, 0)
myColors = (Color.GREEN, Color.WHITE, Color.RED, Color.NONE, Color.LONGE, Color.MAISLONGE)
frontColorSensor.detectable_colors(myColors)

while True:    
    if hub.ble.observe(1) == "garraBaixo":
        garra.run_time(-1000, 1000)
        ooteck2.display.number(44)
        ooteck2.ble.broadcast("garraBaixo")
    elif hub.ble.observe(1) == "garraCima":
        garra.run_time(1000, 1000)
        ooteck2.display.number(33)
        ooteck2.ble.broadcast("garraCima")
    elif hub.ble.observe(1) == "colorSensor":
        if(frontColorSensor.color() == Color.MAISLONGE or frontColorSensor.color() == Color.LONGE):
            ooteck2.ble.broadcast("frente")
        if(frontColorSensor.color() == Color.GREEN or frontColorSensor.color() == Color.RED):
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
