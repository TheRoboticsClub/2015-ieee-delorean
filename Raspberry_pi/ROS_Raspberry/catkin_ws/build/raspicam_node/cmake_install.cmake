# Install script for directory: /home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/src/raspicam_node

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/raspicam_node" TYPE FILE FILES "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/devel/include/raspicam_node/CameraConfig.h")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/raspicam_node" TYPE FILE FILES "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/devel/lib/python2.7/dist-packages/raspicam_node/__init__.py")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  execute_process(COMMAND "/usr/bin/python" -m compileall "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/devel/lib/python2.7/dist-packages/raspicam_node/cfg")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/raspicam_node" TYPE DIRECTORY FILES "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/devel/lib/python2.7/dist-packages/raspicam_node/cfg")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/build/raspicam_node/catkin_generated/installspace/raspicam_node.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/raspicam_node/cmake" TYPE FILE FILES
    "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/build/raspicam_node/catkin_generated/installspace/raspicam_nodeConfig.cmake"
    "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/build/raspicam_node/catkin_generated/installspace/raspicam_nodeConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/raspicam_node" TYPE FILE FILES "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/src/raspicam_node/package.xml")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/raspicam_node" TYPE EXECUTABLE FILES "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/devel/lib/raspicam_node/raspicam_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node"
         OLD_RPATH "/opt/ros/kinetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/raspicam_node/raspicam_node")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/raspicam_node" TYPE DIRECTORY FILES
    "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/src/raspicam_node/launch"
    "/home/delorean/Escritorio/GitHub/2015-ieee-delorean/Raspberry_pi/ROS_Raspberry/catkin_ws/src/raspicam_node/camera_info"
    )
endif()

