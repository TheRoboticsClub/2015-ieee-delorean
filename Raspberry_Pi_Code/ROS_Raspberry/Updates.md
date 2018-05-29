27, May 2018-------------------------------------------------------------------------------------------------------------------

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


28, May 2018----------------------------------------------------------------------------------------------------------

Today we made another gps odometry node. Finally, we were able to calculate heading and distance between 2 gps coordinate points
using python.
Now we have to implement this tool into a ROS python script. We have to save the current gps position and the old gps position from
an older point in time so we can calculate de bearing and distance.

We were able to make the ROS python scripts. It takes the difference between 2 points separated 1 second. It should
calculate de distance between the 2 points and the bearing in degrees. Testing is pending.


29, May 2018----------------------------------------------------------------------------------------------------------

Today we started gps_path_planer node. This node, as it is now, takes one coordinate point from command arguments and gets the distance between that coordinate and the actual car position. Also, if the distance is less that 5 meters, it prints
an alert on the output. So, now we have this nodes about gps:

nmea_serial_driver <---this node it´s simply the gps serial driver. Gives fixes in /fix topic

topic_tools relay  <---this node redirects messages from /fix to /gps/fix

gps_distance_bearing  <---this node gives the distance and bearing between 2 points separated 1 second (it gives information about the car heading and the distance traveled on 1 second). Publishes on /gps/bearing and /gps/distance

gps_odometry_vel <--- same as before but the operations are done by looking into /vel topic data from the serial driver.
We are not very sure if this node will do well.

gps_path_planner <--- this node will take a coordinate point given by command line and calculate the distance and bearing between the car position and that point. In the next days, we will try to make the node do basic navigation (publish Twist messages based on bearing and distance calculated on this node)




