#!/usr/bin/env python
import sys


class Getch:
    def __init__(self):
        import tty

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

getch = Getch()

print("Starting!")
print("Introduzca un comnado")



command = ''

while True:
    comando = getch()
    print(comando)
    if comando == '1':
        sys.exit('Saliendo!')


