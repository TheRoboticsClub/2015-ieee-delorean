DIARIO VITACORA

Vamos a ver como conectarnos con la raspberry, usando ros al ordenador donde tenemos el juego de la tortuga.

>>ssh raspiros@10.1.135.134

Lanzamos en una termnial nueva:

>>roscore


Vamos a aniadir la direccion ip del ordenador donde esta la tortu

>>sudo nano /etc/hosts

probamos que la concexion funcione

>>ping -c 1 delorean-OptiPlex-755


y usamos el juego


SERVER


>>export ROS_MASTER_URI=http://delorean-OptiPlex-755:11311 --> NOMBRE SERVIDOR

CLIENT

>>export ROS_MASTER_URI=http://delorean-OptiPlex-755:11311  --> NOMBRE SERVIDOR

>>rosrun turtlesim turtle_teleop_key


