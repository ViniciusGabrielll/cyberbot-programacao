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

sensorDir = ColorSensor(Port.F)
sensorEsq = ColorSensor(Port.C)

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

cronometro = StopWatch()
fazerCurva = True

# ligar componentes

ultrasonico.lights.on()
ultrasonicoLado.lights.on()

# funcoes

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


def girarGrausVeloDife(graus, velocidade1, velocidade2):
    hub.imu.reset_heading(0)
    if graus > 0:
        while(hub.imu.heading() >= graus * -1):
            motorDir.dc(velocidade1)
            motorEsq.dc(velocidade2)
    else:
        while(hub.imu.heading() <= graus * -1):
            motorDir.dc(velocidade1)
            motorEsq.dc(velocidade2)
    
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
    wait(500)
    if(sensorDir.color() == Color.GREEN and sensorEsq.color() == Color.GREEN):
        while (sensorDir.color() == Color.GREEN):
            motorDir.dc(40)
            motorEsq.dc(40)
        Drive.straight(10)
        Drive.stop()
        wait(100)
        if(sensorEsq.reflection() <= 25):
            print("BECO SEM SAIDA")
            Drive.straight(80)
            girarGraus(180, 80)
        elif(sensorEsq.color() == Color.WHITE):
            print("BRANCO FRENTE")
            Drive.straight(30)
    elif(sensorDir.color() == Color.GREEN and sensorEsq.color() != Color.GREEN):
        print("direito verde")
        while (sensorDir.color() == Color.GREEN):
            motorDir.dc(40)
            motorEsq.dc(40)
        Drive.straight(10)
        Drive.stop()
        wait(100)
        if(sensorDir.reflection() <= 25):
            print("PRETO FRENTE")
            Drive.straight(50)
            girarGrausVeloDife(-90, -100, 70)
            Drive.stop()
            wait(100)
            if(sensorEsq.color() == Color.WHITE):
                while sensorEsq.color() == Color.WHITE:
                    mover(70)
            else:
                print("Pode ir para direita")
            Drive.stop()
        else:
            print("BRANCO FRENTE")
            Drive.straight(30)
    elif(sensorEsq.color() == Color.GREEN and sensorDir.color() != Color.GREEN):
        print("esquerdo verde")
        while (sensorEsq.color() == Color.GREEN):
            motorDir.dc(40)
            motorEsq.dc(40)
        Drive.straight(10)
        Drive.stop()
        wait(100)
        if(sensorEsq.reflection() <= 25):
            print("PRETO FRENTE")
            Drive.straight(50)
            girarGrausVeloDife(90, 70, -100)
            Drive.stop()
            wait(100)
            if(sensorEsq.color() == Color.WHITE):
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
    else:
        Drive.straight(-10)
        if(sensorDir.color() != Color.GREEN and sensorEsq.color() != Color.GREEN):
            Drive.straight(20)
            if(sensorDir.color() != Color.GREEN and sensorDir.color() != Color.GREEN):
                return
        else:
            return




def curvas():
    while(sensorDir.color() != Color.BLACK and sensorEsq.color() != Color.BLACK):
        motorDir.dc(-50)
        motorEsq.dc(-50)
    Drive.stop()
    wait(100)
    if(sensorDir.reflection() < sensorEsq.reflection()):
        Drive.stop()
        print("Curva para Direita")
        Drive.straight(40)
        hub.imu.reset_heading(0)
        while(sensorEsq.color() != Color.GRAY and hub.imu.heading() < 70):
            motorDir.dc(-90)
            motorEsq.dc(90)
        Drive.stop()
        Drive.straight(-30)
        Drive.turn(10)
        Drive.stop()
        wait(100)
    else:
        print("Curva para Esquerda")
        Drive.stop()
        Drive.straight(40)
        hub.imu.reset_heading(0)
        while(sensorDir.color() != Color.GRAY and hub.imu.heading() < 70):
            motorDir.dc(90)
            motorEsq.dc(-90)
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
    Drive.straight(-20)
    while(sensorDir.color() != Color.GRAY):
        motorDir.dc(70)
        motorEsq.dc(-70)
    while(sensorEsq.color() != Color.GRAY):
        motorEsq.dc(70)
        motorDir.dc(-70)
    while(sensorDir.color() != Color.GRAY):
        motorDir.dc(70)
        motorEsq.dc(-70)
    Drive.stop()
    hub.imu.reset_heading(0)
    while ultrasonicoLado.distance() > 70 and hub.imu.heading() < 90:
        mover(-100)
    motorDir.dc(70)
    motorEsq.dc(70)
    wait(500)

    while viuPreto == False:
        if(ultrasonicoLado.distance() <= 150):
            print(ultrasonico.distance())
            motorDir.dc(60)
            motorEsq.dc(60)
        else:
            hub.speaker.beep()
            Drive.straight(30)
            girarGraus(90, 70)
            while(ultrasonicoLado.distance() >= 150 and viuPreto == False):
                motorDir.dc(70)
                motorEsq.dc(70)
                if(sensorEsq.color() == Color.BLACK or sensorEsq.color() == Color.GRAY):
                    viuPreto = True
                    print("Viu preto")
                    Drive.straight(60)
                    
                    while sensorDir.color() != Color.GRAY:
                        motorDir.dc(-100)
                        motorEsq.dc(100)
                    Drive.straight(-30)
    print("Acabou")

def vermelho():
    if(sensorDir.color() == Color.RED and sensorEsq.color() == Color.RED):
        Drive.stop()
        SystemExit()

# fora da mesa
def mover(GIRO):
    motorDir.dc(GIRO)
    motorEsq.dc(-GIRO)




#    RESGATE



ehAEntradaDoResgate = True
vezesSoltar = 0
lado = True
trajetoTerminado = False;
veloPadrao = 100
saida = False

def soltar():
    global vezesSoltar
    global lado
    global trajetoTerminado

    print("soltar")
    vezesSoltar += 1

    motorDir.dc(100)
    motorEsq.dc(100)
    wait(200)
    Drive.straight(-20)
    girarGraus(180, 100)
    Drive.stop()
    
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(250)
    motorDir.dc(100)
    motorEsq.dc(100)
    wait(50)
    Drive.stop()
    hub.ble.broadcast("abrirCompartimento")
    wait(1000)
    hub.ble.broadcast("garraBaixo")
    wait(1000)
    motorDir.dc(100)
    motorEsq.dc(100)
    wait(100)
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(150)

    hub.ble.broadcast("garraCima")
    wait(1000)
    hub.ble.broadcast("fecharCompartimento")
    wait(1000)
    hub.ble.broadcast("none")
    if(vezesSoltar >= 2):
        motorDir.dc(100)
        motorEsq.dc(100)
        wait(200)
        while(ultrasonicoLado.distance() >= 150):
            mover(100)
        trajetoTerminado = True
    elif(lado == True):
        Drive.straight(200)
        print("Girando")
        girarGraus(25, 70)
        lado = False
    else:
        Drive.straight(200)
        print("Girando")
        girarGraus(-25, 70)
        lado = True

def virar():
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(200)
    Drive.stop()
    hub.ble.broadcast("garraCima")
    wait(1000)
    hub.ble.broadcast("none")
    Drive.stop()
    motorDir.dc(100)
    motorEsq.dc(100)
    wait(700)
    Drive.stop()
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(50)
    
    # 1
    Drive.stop()
    hub.ble.broadcast("colorSensor")
    Drive.stop()
    wait(500)
    if(ooteck2.ble.observe(2) == "soltar"):
        soltar() 
        return
    hub.ble.broadcast("none")

    # 2
    motorDir.dc(100)
    motorEsq.dc(-100)
    wait(100)
    Drive.stop()
    hub.ble.broadcast("colorSensor")
    Drive.stop()
    wait(500)    
    if(ooteck2.ble.observe(2) == "soltar"):
        soltar()
        return
    hub.ble.broadcast("none")
    # 3
    motorDir.dc(-100)
    motorEsq.dc(100)
    wait(200)
    Drive.stop()
    hub.ble.broadcast("colorSensor")
    Drive.stop()
    wait(500)
    if(ooteck2.ble.observe(2) == "soltar"):
        soltar() 
        return
    hub.ble.broadcast("none")

    # finish

    motorDir.dc(100)
    motorEsq.dc(-100)
    wait(100)
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(200)
    Drive.stop()
    girarGraus(180, veloPadrao)
    Drive.stop()
    motorDir.dc(-70)
    motorEsq.dc(-70)
    wait(300)
    hub.ble.broadcast("garraBaixo")
    wait(1000)
    hub.ble.broadcast("none")

estaNoResgate = False

def inicio():
    global lado
    global estaNoResgate
    estaNoResgate = True
    if(ultrasonicoLado.distance() <= 100):
        girarGraus(-20, 100)
        motorDir.dc(100)
        motorEsq.dc(100)
        wait(300)
        girarGraus(-70, 100)
        Drive.stop()
        lado = False
    else:
        girarGraus(20, 100)
        motorDir.dc(100)
        motorEsq.dc(100)
        wait(300)
        girarGraus(70, 100)
        Drive.stop()
        lado = True
    motorDir.dc(-70)
    motorEsq.dc(-70)
    wait(1500)

def prataOuPreto():
    print("PRETO OU PRATA")
    Drive.stop()
    if(sensorDir.color() == Color.PRATA or sensorEsq.color() == Color.PRATA):
        prata()
    elif(sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK):
        preto()

def saidaAoLado():
    girarGraus(120, 100)
    timer = StopWatch()
    timer.reset()
    while sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE and timer.time() < 3000:
        motorDir.dc(100)
        motorEsq.dc(100)
    Drive.stop()


def prata():
    print("PRATA")
    Drive.straight(-60)
    girarGraus(-120, 100)
    if(ultrasonico.distance() > 100):
        Drive.straight(250)
    else:
        girarGraus(-90, 100)

def preto():
    global saida
    print("VIU PRETO!!!")
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(200)
    girarGraus(-10, 100)
    motorDir.dc(100)
    motorEsq.dc(100)
    wait(700)
    if sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK:
        saida = True
        return
    girarGraus(30, 100)
    if sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK:
        saida = True
        return
    girarGraus(-60, 100)
    if sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK:
        saida = True
        return
    girarGraus(30, 100)
    saida = True

def andar():
    if ultrasonico.distance() <= 80:
        girarGraus(-15, 100)
    else:
        if(ultrasonicoLado.distance() >= 1900):
            Drive.stop()
            wait(200)
            if(ultrasonicoLado.distance() >= 1900):
                saidaAoLado()
        motorDir.dc(100)
        motorEsq.dc(100)

def saidaNoTrajeto():
    print("SAIDA!")
    Drive.stop()
    wait(100)
    hub.ble.broadcast("garraCima")
    wait(1000)
    motorDir.dc(-100)
    motorEsq.dc(-100)
    wait(1000)
    hub.ble.broadcast("none")
    girarGraus(100, 100)
    hub.ble.broadcast("garraBaixo")
    wait(1000)

def resgate():
    global lado
    inicio()
    while not trajetoTerminado:
        if(sensorDir.color() == Color.PRATA or sensorEsq.color() == Color.PRATA or sensorDir.color() == Color.BLACK or sensorEsq.color() == Color.BLACK):
            print("saida no trajeto")
            saidaNoTrajeto()
        hub.ble.broadcast("garraBaixo")
        wait(1000)
        hub.ble.broadcast("none")
        Drive.stop()
        if(ultrasonico.distance() >= 220 and lado == False):
            motorDir.dc(100)
            motorEsq.dc(90)
        elif(ultrasonico.distance() >= 220 and lado == True):
            motorDir.dc(90)
            motorEsq.dc(100)  
        else:
            motorDir.dc(100)
            motorEsq.dc(100)
            wait(200)
            motorDir.dc(-100)
            motorEsq.dc(-100)
            wait(70)
            Drive.straight(-50)
            if(lado == False):
                motorDir.dc(60)
                motorEsq.dc(100)
                wait(1500)
            else:
                motorDir.dc(100)
                motorEsq.dc(60)
                wait(1500)
            virar()
            if lado == False: 
                lado = True
            else:
                lado = False

    hub.ble.broadcast("garraCima")
    wait(1000)
    hub.ble.broadcast("none")

    while not saida:
        andar()
        if(sensorDir.color() != Color.WHITE and sensorEsq.color() != Color.WHITE):
            while sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE:
                motorDir.dc(-50)
                motorEsq.dc(-50)
            Drive.straight(5)
            Drive.stop()
            prataOuPreto()
    return

        


# linha de repeticao
while True:
    if(sensorDir.color() == Color.RED and sensorEsq.color() == Color.RED):
        vermelho()
    elif(sensorDir.color() == Color.GREEN or sensorEsq.color() == Color.GREEN):
        Drive.stop()
        print("verde")
        while (sensorDir.color() != Color.GREEN and sensorEsq.color() != Color.GREEN):
            motorDir.dc(-70)
            motorEsq.dc(-70)
        Drive.straight(-5)
        verde()
    else:
        # esta inclinado
        incX, incY = hub.imu.tilt()
        if(incX >= 10):
            if(ooteck2.ble.observe(2) != "garraBaixo"):
                hub.ble.broadcast("garraBaixo")
            segueLinha(0.5, 0, 0, 100)
            if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                motorDir.dc(70)
                motorEsq.dc(70)
        else:
            if(ooteck2.ble.observe(2) != "garraCima"):
                Drive.stop()
                hub.ble.broadcast("garraCima")
            # linha principal
            if(ultrasonico.distance() <= 50):
                obstaculo()
            elif((((sensorEsq.color() == Color.WHITE or sensorEsq.color() == Color.GRAY) and sensorDir.color() == Color.BLACK) or ((sensorDir.color() == Color.WHITE or sensorDir.color() == Color.GRAY) and sensorEsq.color() == Color.BLACK)) and fazerCurva == True):
                motorDir.dc(100)
                motorEsq.dc(100)
                wait(200)
                Drive.stop()
                if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                    curvas()
                    fazerCurva = False
                else:
                    motorDir.dc(-100)
                    motorEsq.dc(-100)
                    wait(200)
                    fazerCurva = False
                    cronometro.reset()
            else:
                segueLinha(4, 3, 3, 70)
            if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                motorDir.dc(100)
                motorEsq.dc(100)

            if(ultrasonicoLado.distance() < 100 and ehAEntradaDoResgate == True):
                Drive.straight(20)
                Drive.stop()
                wait(50)
                if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                    girarGraus(20, 70)
                    if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                        girarGraus(-40, 70)
                        if(sensorDir.color() == Color.WHITE and sensorEsq.color() == Color.WHITE):
                            girarGraus(20, 70)
                            resgate()
                if(estaNoResgate == False):
                    Drive.straight(-60)
                    ehAEntradaDoResgate = False
                    cronometro.reset()

            if not ehAEntradaDoResgate and cronometro.time() >= 3000:
                ehAEntradaDoResgate = True 
            if not fazerCurva and cronometro.time() >= 1000:
                fazerCurva = True