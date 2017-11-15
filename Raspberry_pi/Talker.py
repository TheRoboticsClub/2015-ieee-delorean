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

def movimiento(tipo, pub, signo):

    if tipo == 'angular':
        mensaje = Twist()
        mensaje.angular.z = 1.0*signo
        rospy.loginfo(mensaje)
        pub.publish(mensaje)

    elif tipo == 'lineal':

        mensaje = Twist()
        mensaje.linear.x = 1.0*signo
        rospy.loginfo(mensaje)
        pub.publish(mensaje)




def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('controlteclas', anonymous=True)
    while not rospy.is_shutdown():

        getch = Getch()
        comando = getch()
        print(comando)
        if comando == '1':
            sys.exit('Saliendo!')

        if comando == 'w':
            movimiento('lineal', pub, 1)

        elif comando == 'a':
            movimiento('angular', pub, 1)
        
        elif comando == 's':
            movimiento('lineal', pub, -1)
        
        elif comando == 'd':
            movimiento('angular', pub, -1)        
            

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
