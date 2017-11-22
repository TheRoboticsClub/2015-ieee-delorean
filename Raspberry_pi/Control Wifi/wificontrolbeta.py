# -*- coding: utf-8 -*-
import serial

class Getch:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def set_angulo(angulo,valor):

    angulo += valor

    if angulo > 180:
        angulo = 180
    elif angulo < 0:
        angulo = 0

    return angulo

def set_speed(speed,valor,capado):

    speed += valor

    if speed > 1600 and capado == True:
        speed = 1600
    elif speed < 1450 and capado == True:
        speed = 1450

    return speed



arduino = serial.Serial('/dev/ttyUSB0', 9600)

getch = Getch()

print("Starting!")
print("Introduzca un comnado")


speed = 0 #Velocidad del coche
w = 90 #Ángulo de giro, 90 es el medio.
capado = True 

command = ''

while True:
    comando = getch()
    #comando = raw_input('Introduce un comando: ') #Input
    if comando == 'w':
        speed = set_speed(speed,5,capado) 
        command = str(speed)
        
        print('ADELANTE')
    elif comando == 's':
        speed = set_speed(speed,-5,capado)
        command = str(speed)

        print('ATRAS')
    elif comando == 'a':
        w = set_angulo(w,-3)

        command = str(w)
        print('IZQUIERDA')

    elif comando == 'd':
        w = set_angulo(w,3)
        command = str(w)
        print('DERECHA')

    elif comando == ' ':
        speed = 1500
        command = str(speed)

    elif comando == 'v':
        capado = False

    elif comando == 'c':
        capado = True
    elif comando == 't':
        w = 90
        command = str(w)
        print ('RECTO')

    else: 
        continue

    arduino.write(command) #con esto paso la instrucción a la raspberry
    print(command)





arduino.close() #Finalizamos la comunicacion
