#!/bin/bash
# Update package list first
sudo apt-get update

# Remove the broken sdformat_urdf plugin so robot_state_publisher doesn't crash.
# It tries to dlopen libsdformat14.so.14, which isn't present in this image, which
# kills robot_state_publisher -> /robot_description never publishes -> controllers
# never spawn. The UR driver uses plain URDF/xacro, so this plugin isn't needed.
sudo apt-get remove -y ros-jazzy-sdformat-urdf || true

# Install system and Python dependencies
sudo apt-get install -y python3-scipy python3-torch python3-matplotlib python3-torchvision
# Install any other dependencies your src/ folder needs
rosdep update
rosdep install --from-paths src --ignore-src -r -y
sudo apt update && \
   sudo apt install -y ros-jazzy-controller-manager ros-jazzy-controller-interface ros-jazzy-hardware-interface && \
   rosdep update && \
   rosdep install --from-paths ${ISAAC_ROS_WS}/src/Universal_Robots_ROS2_Driver --ignore-src -y
cd ${ISAAC_ROS_WS} && \
   colcon build --symlink-install --packages-up-to ur_robot_driver && source install/setup.bash
sudo apt-get install -y curl jq tar
