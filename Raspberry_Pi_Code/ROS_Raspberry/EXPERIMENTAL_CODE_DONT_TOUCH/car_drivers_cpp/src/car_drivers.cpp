#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <sstream>
#include <time.h>
#include <thread>
using namespace std;


class vel_pub_subscriber{

public:

  vel_pub_subscriber(ros::NodeHandle n, ros::Publisher pub)
  {
    n_ = n;
    pub_ = pub;
    sub_ = n_.subscribe("/car1/cmd_vel", 10, &vel_pub_subscriber::cmd_vel_callback, this);
  }

  void cmd_vel_callback(const geometry_msgs::Twist::ConstPtr& msg)
  {
    ROS_INFO("CMD_VEL CALLBACK [%f]", msg->linear.x);
    pub_.publish(msg);
  }

private:
  ros::NodeHandle n_;
  ros::Publisher pub_;
  ros::Subscriber sub_;

};


class Timer{

public:

  bool arrived;
  double dt;
  time_t old_time;
  time_t time_now;

  Timer(){

    dt = 100;
    arrived = false;
    time(&old_time);
    time(&time_now);

  }

};


class ping_subscriber{

public:

  ping_subscriber(ros::NodeHandle n, Timer& timer){

    n_ = n;
    sub_ = n_.subscribe("/ping", 10, &ping_subscriber::ping_callback, this);
    timer_ = timer;

  }

  void ping_callback(const std_msgs::String::ConstPtr& msg){
    timer_.arrived = true;
  }

private:

  ros::NodeHandle n_;
  ros::Subscriber sub_;
  Timer timer_;

};

void ping_verifier(Timer& timer){


  while(1){

    if(timer.arrived){

      timer.old_time = timer.time_now;
      timer.arrived = false;
    }

    time(&timer.time_now);
    timer.dt = difftime(timer.time_now, timer.old_time);

    if(timer.dt >= 3){
      __asm__("nop");//todo
    }


  }


}


int main(int argc, char **argv)
{

  ros::init(argc, argv, "car_drivers");

  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<geometry_msgs::Twist>("/arduino/cmd_vel", 10);

  Timer timer;
  vel_pub_subscriber vel_subscriber(n, pub);
  ping_subscriber ping_sub(n, timer);

  auto ping_thread = std::thread(ping_verifier, std::ref(timer));

  ros::spin();

  return 0;
}
