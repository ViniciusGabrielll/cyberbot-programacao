from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()

motorDir = Motor(Port.A)
motorEsq = Motor(Port.B, Direction.COUNTERCLOCKWISE)

sensorDir = ColorSensor(Port.C)
sensorEsq = ColorSensor(Port.D)

ultrasonico = UltrasonicSensor(Port.E)



Drive = DriveBase(motorDir, motorEsq, wheel_diameter=30 ,axle_track=150)


varCalibragem = True

referWhiteDir = 0
referWhiteEsq = 0

hsvWhiteDir = 0
hsvWhiteEsq = 0

referBlackDir = 0
referBlackEsq = 0
    
hsvBlackDir = 0
hsvBlackEsq = 0

def calibragem():
    print()
    print()

    print("-------------------------------")
    print("Coloque no branco: ")
    hub.display.text("BRANCO")
    wait(3000)
    referWhiteDir = sensorDir.reflection()
    referWhiteEsq = sensorEsq.reflection()

    hsvWhiteDir = sensorDir.hsv()
    hsvWhiteEsq = sensorEsq.hsv()

    print()
    print("-------------------------------")
    print("Coloque no preto: ")
    hub.display.text("PRETO")
    wait(3000)
    referBlackDir = sensorDir.reflection()
    referBlackEsq = sensorEsq.reflection()
    
    hsvBlackDir = sensorDir.hsv()
    hsvBlackEsq = sensorEsq.hsv()

    print()
    print("- Valores Calibragem ----------")
    print()
    print("- Reflecao --------------------")
    print("- Branco direito: ", referWhiteDir)
    print("- Branco esquerdo: ", referWhiteEsq)
    print("- Preto direito: ", referBlackDir)
    print("- Preto esquerdo: ", referBlackEsq)
    print()
    print("- HSV -------------------------")
    print("- Branco direito: ", hsvWhiteDir)
    print("- Branco esquerdo: ", hsvWhiteEsq)
    print("- Preto direito: ", hsvBlackDir)
    print("- Preto esquerdo: ", hsvBlackEsq)
    print()
    wait(3000)
    print("calibragem acabada")
    varCalibragem = False

    while(ultrasonico.distance() >= 50):
        print("...")
        wait(500)

calibragem()

Color.WHITE = Color(205, 20, 94) 
Color.GREEN = Color(147, 55, 27)
Color.BLACK = Color(202, 23, 49) 
Color.GRAY = Color(210, 19, 13)
Color.RED = Color(351, 91, 67) 
myColors = (Color.GREEN, Color.WHITE, Color.BLACK, Color.GRAY, Color.RED)
sensorDir.detectable_colors(myColors)
sensorEsq.detectable_colors(myColors)

def verde():
    Drive.stop()
    wait(1000)
    if(sensorDir.color() == Color.GREEN and sensorEsq.color() == Color.GREEN):
        Drive.straight(140)
        Drive.turn(230)
        Drive.straight(40)
    elif(sensorDir.color() == Color.GREEN and sensorEsq.color() != Color.GREEN):
        Drive.straight(-40)
        if(sensorDir.color() == Color.WHITE):
            Drive.straight(80)
            Drive.turn(40)
            while(sensorEsq.color() != Color.BLACK):
                mover(60)
            Drive.straight(-20)
            Drive.stop()
        elif(sensorDir.color() == Color.BLACK):
            Drive.straight(50)
    elif(sensorEsq.color() == Color.GREEN and sensorDir.color() != Color.GREEN):
        Drive.straight(-40)
        if(sensorEsq.color() == Color.WHITE):
            Drive.straight(80)
            Drive.turn(-40)
            while(sensorDir.color() != Color.BLACK):
                mover(-60) 
            Drive.straight(-20)
        elif(sensorEsq.color() == Color.BLACK):
            Drive.straight(50)
        
def vermelho():
    if(sensorDir.color() == Color.RED and sensorEsq.color() == Color.RED):
        Drive.stop()

def segueLinha(KP, KI, KD, velocidadeB):
    erroAnterior = 0
    integral = 0
    erro = sensorDir.reflection() - sensorEsq.reflection()
    integral += erro
    derivativo = erro - erroAnterior
    correcao = (KP * erro) + (KI * integral) + (KD * derivativo)
    velocidadeD = velocidadeB - correcao
    velocidadeE = velocidadeB + correcao
    motorDir.dc(velocidadeD)
    motorEsq.dc(velocidadeE) 
    erroAnterior = erro

def curvas():
    if((sensorDir.reflection() >= 40 and sensorDir.reflection() <= 70) and (sensorEsq.reflection() >= 5 and sensorEsq.reflection() <= 10)):
        Drive.stop()
        wait(2000)
        print("Curva Esquerda")
        Drive.straight(-20)
        while(sensorDir.color() != Color.BLACK):
            mover(70)
        Drive.stop()
        wait(100)
    elif((sensorEsq.reflection() >= 40 and sensorEsq.reflection() <= 70) and (sensorDir.reflection() >= 5 and sensorDir.reflection() <= 10)):
        print("Curva Direita")
        Drive.stop()
        wait(2000)
        Drive.straight(-20)
        while(sensorEsq.color() != Color.BLACK):
            mover(-70)
        Drive.stop()
        wait(100)
            
def mover(GIRO):
    motorDir.dc(GIRO)
    motorEsq.dc(-GIRO)

def obstaculo():
    Drive.stop()
    wait(100)
    ultrasonico.lights.off()
    wait(100)
    ultrasonico.lights.on()
    wait(100)
    ultrasonico.lights.off()
    wait(100)
    ultrasonico.lights.on()
    wait(100)
    Drive.straight(-20)
    Drive.turn(50)
    while(sensorDir.color() != Color.BLACK or sensorEsq.color() != Color.BLACK):
        motorDir.dc(10)
        motorEsq.dc(40) 

varSegueLinha = False;

if(ultrasonico.distance() <= 50):
    print("Segue linha comeca")
    print()
    varSegueLinha = True
    wait(100)
    ultrasonico.lights.off()
    wait(100)
    ultrasonico.lights.on()
    wait(100)
    ultrasonico.lights.off()
    wait(100)
    ultrasonico.lights.on()
    
    hub.display.text("SEGUIR")

    wait(2000)


while varSegueLinha == True:
    if(sensorDir.color() == Color.RED and sensorEsq.color() == Color.RED):
        vermelho()
    elif(sensorDir.color() == Color.GREEN or sensorEsq.color() == Color.GREEN):
        verde()
    else:
        incX, incY = hub.imu.tilt()
        if(incX >= 4 or incX <= -4):
            print("SUBINDO")
            curvas()
            segueLinha(0.5, 0.07, 0.5, 60)
            if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                motorDir.dc(60)
                motorEsq.dc(60)
        else:
            curvas()
            if(sensorDir.color() == Color.BLACK and sensorEsq.color() == Color.WHITE):
                Drive.stop()
                Drive.straight(-10)
            segueLinha(4, 0.07, 0.5, 50)
            if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                motorDir.dc(40)
                motorEsq.dc(40)
            if(ultrasonico.distance() <= 50):
                obstaculo()