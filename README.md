# ROS2 Robot Simulation with Gazebo Sim
This project provides a reproducible workflow for simulating a custom robot in ROS2 using Gazebo Sim (new Gazebo).

## Overview
It demonstrates how to:
- Load a robot model authored in URDF/Xacro
- Publish TF frames using robot_state_publisher (includes plugin from Gazebo Sim)
- Launch Gazebo Sim with a custom render engine (OGRE) for virtualized environments; most apt for running on Virtual Machines (ie. VMware)
- Spawning the robot in Gazebo
- Simulate onboard sensors (Camera) 

## Note
This project is inspired by the work of **joshnewans** and his *Articulated Robotics* blog and tutorial. Many of the design decisions and workflow used were influenced by his ROS2 and Gazebo tutorials.


