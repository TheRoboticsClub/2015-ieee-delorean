#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <sstream>

using namespace std;

int main(int argc, char **argv)
{

  ros::init(argc, argv, "rpi_zero_controller");
  ros::NodeHandle n;
  ros::Publisher vel_pub = n.advertise<geometry_msgs::Twist>("/arduino/cmd_vel", 10);
  ros::Publisher ping_pub = n.advertise<std_msgs::String>("/ping", 10);
  ros::Rate rate(1);


  while(1){

    std_msgs::String msg;
    std::stringstream ss;
    ss << "ping";
    msg.data = ss.str();
    ping_pub.publish(msg);

    geometry_msgs::Twist t_msg;
    t_msg.linear.x = 0.5;
    t_msg.angular.z = 0.5;
    vel_pub.publish(t_msg;)
    rate.sleep();
    ros::spinOnce();
  }

  return 0;
}
