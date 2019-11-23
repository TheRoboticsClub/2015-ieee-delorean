#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <sstream>


class pubSubscriber{

public:

  pubSubscriber(ros::NodeHandle n, ros::Publisher pub)
  {
    n_ = n
    pub_ = pub;
    sub_ = n.subscribe("/car1/cmd_vel", 10, &pubSubscriber::cmd_vel_callback, this);
  }

  void cmd_vel_callback(const geometry_msgs::Twist::ConstPtr& msg)
  {
    ROS_INFO("CMD_VEL CALLBACK [%s]", msg->data.c_str());
    pub_.publish(msg);
  }

private:
  ros::NodeHandle n_;
  ros::Publisher pub_;
  ros::Subscriber sub_;

};



int main(int argc, char **argv)
{

  ros::init(argc, argv, "car_drivers");

  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<geometry_msgs::Twist>("/arduino/cmd_vel", 10);
  pubSubscriber subscriber(n, pub);

  return 0;
}
