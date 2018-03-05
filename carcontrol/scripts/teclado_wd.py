#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys
from geometry_msgs.msg import Twist

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

def movimiento(tipo, pub, valor, estado_coche):

    if tipo == 'angular':

        estado_coche.angular.z = valor
        rospy.loginfo(estado_coche)
        pub.publish(estado_coche)

    elif tipo == 'lineal':

        estado_coche.linear.x = valor
        rospy.loginfo(estado_coche)
        pub.publish(estado_coche)




def talker():
    pub = rospy.Publisher('/turtle1/watch_dog', Twist, queue_size=10)
    rospy.init_node('teclado_wd', anonymous=True)
    estado_coche = Twist()
    estado_coche.linear.x = 0.5
    estado_coche.angular.z = 0.5
    throttle = 0.5
    steering = 0.5
    while not rospy.is_shutdown():

        getch = Getch()
        comando = getch()
        print(comando)
        if comando == '1':
            sys.exit('Saliendo!')

        if comando == 'w':
            throttle = throttle + 0.01
            movimiento('lineal', pub, throttle, estado_coche)

        elif comando == 'a':
            steering = steering - 0.05
            movimiento('angular', pub, steering, estado_coche)
        
        elif comando == 's':
            throttle = throttle - 0.01
            movimiento('lineal', pub, throttle, estado_coche)
        
        elif comando == 'd':
            steering = steering + 0.05
            movimiento('angular', pub, steering, estado_coche)
        
        elif comando == ' ':
            throttle = 0.5
            movimiento('lineal', pub, throttle, estado_coche)
            

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
