# bibliotecas

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# definir

hub = InventorHub()

motorDir = Motor(Port.A)
motorEsq = Motor(Port.B, Direction.COUNTERCLOCKWISE)
Drive = DriveBase(motorDir, motorEsq, wheel_diameter=30 ,axle_track=150)

sensorDir = ColorSensor(Port.D)
sensorEsq = ColorSensor(Port.C)

ultrasonico = UltrasonicSensor(Port.E)
ultrasonicoLado = UltrasonicSensor(Port.F)
Color.WHITE = Color(193, 11, 90) 
Color.GREEN = Color(191, 57, 26)
Color.BLACK = Color(200, 15, 22) 
Color.GRAY = Color(195, 31, 17)
Color.RED = Color(351, 91, 67) 
myColors = (Color.GREEN, Color.WHITE, Color.BLACK, Color.GRAY, Color.RED)
sensorDir.detectable_colors(myColors)
sensorEsq.detectable_colors(myColors)

cronometro = StopWatch()

# ligar componentes

ultrasonico.lights.on()
ultrasonicoLado.lights.on()


# funcoes

def segueLinha(KP, KI, KD, velocidadeB):
    erroAnterior = 0
    integral = 0
    erro = sensorEsq.reflection() - sensorDir.reflection()
    integral += erro
    derivativo = erro - erroAnterior
    correcao = (KP * erro) + (KI * integral) + (KD * derivativo)
    velocidadeD = velocidadeB - correcao
    velocidadeE = velocidadeB + correcao
    motorDir.dc(velocidadeD)
    motorEsq.dc(velocidadeE) 
    erroAnterior = erro

def verde():
    Drive.stop()
    print("verde")
    if(sensorDir.color() == Color.GREEN and sensorEsq.color() == Color.GREEN):
        print("BECO SEM SAIDA")
        Drive.straight(140)
        Drive.turn(230)
        Drive.straight(60)
    elif(sensorDir.color() == Color.GREEN and sensorEsq.color() != Color.GREEN):
        print("direito verde")
        wait(1000)
        Drive.straight(30)
        Drive.stop()
        if(sensorDir.reflection() <= 14):
            print("PRETO FRENTE")
            Drive.straight(30)
            Drive.turn(-90)
            Drive.stop()
            wait(500)
            if(sensorEsq.color() == Color.WHITE):
                print(sensorEsq.color())
                while sensorEsq.color() == Color.WHITE:
                    mover(70)
            else:
                print("Pode ir para esquerda")
            Drive.stop()
        elif(sensorDir.color() == Color.WHITE):
            print("BRANCO FRENTE")
            Drive.straight(30)
    elif(sensorEsq.color() == Color.GREEN and sensorDir.color() != Color.GREEN):
        print("esquerdo verde")
        wait(1000)
        Drive.straight(30)
        print("andei")
        wait(1000)
        Drive.stop()
        if(sensorEsq.reflection() <= 14):
            print("PRETO FRENTE")
            Drive.straight(30)
            Drive.turn(90)
            Drive.stop()
            wait(500)
            if(sensorEsq.color() == Color.WHITE):
                print(sensorEsq.color())
                while sensorEsq.color() == Color.WHITE:
                    mover(-70)
            else:
                print("Pode ir para esquerda")
            Drive.stop()
        elif(sensorEsq.color() == Color.WHITE):
            print("BRANCO FRENTE")
            Drive.straight(30)
        elif(sensorEsq.color() == Color.GREEN):
            Drive.straight(5)
            wait(500)




def curvas():
    Drive.stop()
    wait(100)
    if((sensorEsq.reflection() >= 60 and sensorEsq.reflection() <= 75) and (sensorDir.reflection() >= 25 and sensorDir.reflection() <= 40) and sensorDir.color() != Color.GREEN):
        Drive.stop()
        wait(200)
        print("Curva para Direita")
        Drive.straight(40)
        hub.imu.reset_heading(0)
        while(sensorEsq.color() != Color.GRAY and hub.imu.heading() < 70):
            motorDir.dc(-60)
            motorEsq.dc(60)
        Drive.stop()
        Drive.straight(-30)
        Drive.turn(10)
        Drive.stop()
        wait(100)
    elif((sensorDir.reflection() >= 60 and sensorDir.reflection() <= 75) and (sensorEsq.reflection() >= 30 and sensorEsq.reflection() <= 50) and sensorEsq.color() != Color.GREEN):
        print("Curva para Esquerda")
        Drive.stop()
        wait(200)
        Drive.straight(40)
        hub.imu.reset_heading(0)
        while(sensorDir.color() != Color.GRAY and hub.imu.heading() < 70):
            motorDir.dc(60)
            motorEsq.dc(-60)
        Drive.stop()
        Drive.straight(-30)
        Drive.turn(-10)
        Drive.stop()
        wait(100)


def obstaculo():
    viuPreto = False
    Drive.stop()
    hub.light.off()
    wait(100)
    ultrasonico.lights.off()
    wait(100)
    ultrasonico.lights.on()
    wait(100)
    ultrasonico.lights.off()
    wait(100)
    ultrasonico.lights.on()
    wait(100)
    Drive.straight(-40)
    while(sensorDir.color() != Color.GRAY):
        motorDir.dc(50)
        motorEsq.dc(-50)
    while(sensorEsq.color() != Color.GRAY):
        motorEsq.dc(50)
        motorDir.dc(-50)
    Drive.stop()

    girarGraus(-76, 70)
    Drive.straight(50)
    while viuPreto == False:
        if(ultrasonicoLado.distance() <= 200):
            print(ultrasonico.distance())
            motorDir.dc(50)
            motorEsq.dc(50)
        else:
            Drive.straight(50)
            hub.speaker.beep()
            girarGraus(89, 70)
            while(ultrasonicoLado.distance() >= 200 and viuPreto == False):
                print(ultrasonico.distance())
                motorDir.dc(50)
                motorEsq.dc(50)
                if(sensorEsq.color() == Color.BLACK or sensorEsq.color() == Color.GRAY):
                    viuPreto = True
                    print("Viu preto")
                    Drive.straight(60)
                    girarGraus(-80, 70)
                    Drive.straight(-50)
    print("Acabou")

def vermelho():
    if(sensorDir.color() == Color.RED and sensorEsq.color() == Color.RED):
        Drive.stop()

# fora da mesa
def mover(GIRO):
    motorDir.dc(GIRO)
    motorEsq.dc(-GIRO)

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

# linha de repeticao
while True:
    if(sensorDir.color() == Color.RED and sensorEsq.color() == Color.RED):
        vermelho()
    elif(sensorDir.color() == Color.GREEN or sensorEsq.color() == Color.GREEN):
        verde()
    else:
        # esta inclinado
        incX, incY = hub.imu.tilt()
        if(incX >= 4):
            print("SUBINDO")
            segueLinha(1, 0, 0, 70)
            if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                motorDir.dc(70)
                motorEsq.dc(70)
        else:
            # linha principal
            if(ultrasonico.distance() <= 50):
                obstaculo()
            if((sensorEsq.reflection() >= 65 and sensorEsq.reflection() <= 70) and (sensorDir.reflection() >= 25 and sensorDir.reflection() <= 30)) or \
            ((sensorDir.reflection() >= 70 and sensorDir.reflection() <= 75) and (sensorEsq.reflection() >= 30 and sensorEsq.reflection() <= 50)):
                curvas()
            else:
                segueLinha(5, 2, 2, 80)
            if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                motorDir.dc(40)
                motorEsq.dc(40)

            if(ultrasonicoLado.distance() < 100 and ehAEntradaDoResgate == True):
                Drive.straight(40)
                Drive.stop()
                wait(50)
                if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                    print("Resgate")
                    Drive.stop()
                    wait(10000000)
                else:
                    Drive.straight(-40)
                    ehAEntradaDoResgate = False
                    cronometro.reset()

            if not ehAEntradaDoResgate and cronometro.time() >= 3000:
                ehAEntradaDoResgate = True   