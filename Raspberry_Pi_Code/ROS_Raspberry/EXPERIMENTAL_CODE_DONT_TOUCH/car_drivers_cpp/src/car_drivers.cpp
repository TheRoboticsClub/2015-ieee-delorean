#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <sstream>
#include <time.h>
#include <thread>
#include <chrono>
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
  int debug_int;

  Timer(){

    dt = 100;
    arrived = false;
    time(&old_time);
    time(&time_now);
    debug_int = 0;

  }

};


class ping_subscriber{

public:

  ping_subscriber(ros::NodeHandle n, Timer *timer){

    n_ = n;
    sub_ = n_.subscribe("/ping", 10, &ping_subscriber::ping_callback, this);
    timer_ = timer;

  }

  void ping_callback(const std_msgs::String::ConstPtr& msg){
    //ROS_INFO("PING ARRIVED");
    timer_->arrived = true;
    ROS_INFO("[%i]", timer_->debug_int);
  }

private:

  ros::NodeHandle n_;
  ros::Subscriber sub_;
  Timer *timer_;

};

void ping_verifier(Timer& timer, ros::Publisher& vel_pub){

  while(1){

    if(timer.arrived){

      timer.old_time = timer.time_now;
      timer.arrived = false;
     // ROS_INFO("INSIDE CONDITION");
    }

    time(&timer.time_now);
    //ROS_INFO("TIME NOW: [%f]", timer.time_now);
    //ROS_INFO("OLD TIME: [%f]", timer.old_time);
    timer.dt = difftime(timer.time_now, timer.old_time);
    ROS_INFO("DT is: [%f]", timer.dt);

    if(timer.dt >= 3){
      //ROS_INFO("PING DINT'T ARRIVE IN TIME");
      geometry_msgs::Twist t_msg;
      t_msg.linear.x = 0.5;
      t_msg.angular.z = 0.5;
      vel_pub.publish(t_msg);

    }

    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

  }

}


int main(int argc, char **argv)
{

  ros::init(argc, argv, "car_drivers");

  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<geometry_msgs::Twist>("/arduino/cmd_vel", 10);

  Timer timer;
  vel_pub_subscriber vel_subscriber(n, pub);
  ping_subscriber ping_sub(n, &timer);

  auto ping_thread = std::thread(ping_verifier, std::ref(timer), std::ref(pub));

  ros::spin();

  return 0;
}
