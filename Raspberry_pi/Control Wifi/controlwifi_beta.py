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

arduino = serial.Serial('/dev/ttyACM0', 9600)

getch = Getch()

print("Starting!")
print("Introduzca un comnado")


speed = 0 #Velocidad del coche
w = 90 #Ángulo de giro, 90 es el medio.

command = ''

while True:
    comando = getch()
    print 'caca'
    #comando = raw_input('Introduce un comando: ') #Input
    if comando == 'w':
        speed += 10 
        command = 'move.%d' % speed
        
        print('LED ENCENDIDO')
    elif comando == 's':
        
        speed -= 10
        command = 'move.%d' % speed

        print('LED APAGADO')
    elif comando == 'a':
        w =set_angulo(w,-5)

        command = 'turn.%d' % w


    elif comando == 'd':
        w =set_angulo(w,5)
        command = 'turn.%d' % w

    elif comando == ' ':
        command = 'stop'
        speed = 0

    else: 
        continue

    arduino.write(command) #con esto paso la instrucción a la raspberry






arduino.close() #Finalizamos la comunicacion
