27, May 2018

It was mandatory to make the new created launch file launch at start of the system. In order to do that, the following had to be
done:

rosrun robot_upstart install car_drivers/launch/car_drivers.launch

sudo systemctl daemon-reload && sudo systemctl start car

this launches the car_drivers.launch at startup. There is a problem with the ttyUSB0 at start, wich produces a permission denied
error. To solve this, a file must be created:

sudo nano /etc/udev/rules.d/40-permission.rules

the file must contain the following line:

KERNEL=="ttyUSB0", MODE="0666"

That way the launch file and all its nodes should be launched without problem at start.

The launch file we created runs:

-Arduino node
-Car watchdog node
-rosbridge web node

This allows us to have the car ready to run at start, whete it is controlled by the web browser interface or another
ros controller node like ps3 controller
