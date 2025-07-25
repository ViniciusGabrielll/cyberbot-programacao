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
Color.BLACK = Color(200, 15, 22) 
Color.GRAY = Color(195, 31, 17)
Color.RED = Color(351, 91, 67) 
Prata = Color(206, 24, 78)
myColors = (Color.GREEN, Color.WHITE, Color.BLACK, Color.GRAY, Color.RED, Prata)
sensorDir.detectable_colors(myColors)
sensorEsq.detectable_colors(myColors)

vezesSoltar = 0
lado = True
trajetoTerminado = False;
veloPadrao = 100
saida = False

# ligar componentes

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

def soltar():
    global vezesSoltar
    global lado
    global trajetoTerminado

    print("soltar")
    vezesSoltar += 1

    Drive.straight(-150)
    Drive.stop()
    if(lado == True):
        motorDir.dc(30)
        motorEsq.dc(veloPadrao)
        wait(1000)
        motorDir.dc(veloPadrao)
        motorEsq.dc(30)
        wait(1000)
    else:
        motorDir.dc(veloPadrao)
        motorEsq.dc(30)
        wait(1000)
        motorDir.dc(30)
        motorEsq.dc(veloPadrao)
        wait(1000)
    Drive.straight(-20)
    girarGraus(180, 70)
    Drive.stop()
    Drive.straight(-50)
    Drive.straight(20)
    hub.ble.broadcast("abrirCompartimento")
    wait(1000)
    hub.ble.broadcast("garraBaixo")
    wait(1000)
    hub.ble.broadcast("garraCima")
    wait(1000)
    hub.ble.broadcast("fecharCompartimento")
    wait(1000)
    Drive.straight(200)
    if(vezesSoltar >= 3):
        trajetoTerminado = True
    elif(lado == True):
        print("Girando")
        girarGraus(25, 70)
        lado = False
    else:
        print("Girando")
        girarGraus(-25, 70)
        lado = True

def virar():
    Drive.straight(-50)
    Drive.stop()
    hub.ble.broadcast("garraCima")
    wait(1000)
    Drive.stop()
    hub.ble.broadcast("none")
    Drive.straight(200)
    Drive.stop()
    Drive.straight(-25)
    
    # 1
    Drive.stop()
    hub.ble.broadcast("colorSensor")
    Drive.stop()
    if(ooteck2.ble.observe(2) == "soltar"):
        soltar() 
        return
    wait(500)

    # 2
    motorDir.dc(70)
    motorEsq.dc(-70)
    wait(150)
    Drive.stop()
    hub.ble.broadcast("colorSensor")
    Drive.stop()
    if(ooteck2.ble.observe(2) == "soltar"):
        soltar()
        return
    wait(500)    
    # 3
    motorDir.dc(-70)
    motorEsq.dc(70)
    wait(300)
    Drive.stop()
    hub.ble.broadcast("colorSensor")
    Drive.stop()
    if(ooteck2.ble.observe(2) == "soltar"):
        soltar() 
        return
    wait(500)
    # finish

    motorDir.dc(70)
    motorEsq.dc(-70)
    wait(150)
    Drive.straight(-20)
    hub.ble.broadcast("none")
    Drive.stop()
    girarGraus(180, veloPadrao)
    Drive.stop()
    motorDir.dc(-70)
    motorEsq.dc(-70)
    wait(300)
    hub.ble.broadcast("garraBaixo")
    wait(1000)
    hub.ble.broadcast("none")

def inicio():
    global lado
    if(ultrasonicoLado.distance() <= 100):
        girarGraus(-90, 100)
        Drive.stop()
        lado = False
    else:
        girarGraus(90, 100)
        Drive.stop()
        lado = True
    motorDir.dc(-70)
    motorEsq.dc(-70)
    wait(1000)

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
        while sensorDir.color() != Color.WHITE:
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

def saidaNoTrajeto():
    hub.ble.broadcast("garraCima")
    wait(1000)
    girarGraus(200, 100)
    hub.ble.broadcast("garraBaixo")
    wait(1000)

inicio()

while not trajetoTerminado:
    hub.ble.broadcast("garraBaixo")
    wait(1000)
    Drive.stop()

    if(sensorDir.color() == Prata or sensorEsq.color() == Prata or sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK):
        saidaNoTrajeto
    elif(ultrasonico.distance() >= 220 and lado == False):
        motorDir.dc(veloPadrao)
        motorEsq.dc(80)
    elif(ultrasonico.distance() >= 220 and lado == True):
        motorDir.dc(80)
        motorEsq.dc(veloPadrao)  
    else:
        Drive.straight(70)
        Drive.straight(-50)
        if(lado == False):
            motorDir.dc(veloPadrao)
            motorEsq.dc(60)
            wait(1000)
        else:
            motorDir.dc(veloPadrao)
            motorEsq.dc(60)
            wait(1000)
        virar()
        if lado == False: 
            lado = True
        else:
            lado = False


while not saida:
    andar()
    if(sensorDir.color() != Color.WHITE or sensorEsq.color() != Color.WHITE):
        prataOuPreto()
    if(ultrasonicoLado.distance() >= 1900):
        saidaAoLado()