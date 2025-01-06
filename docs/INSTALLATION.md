# Installation Guide

## Getting this repository
This repository is intended to be used as a ROS2 colcon workspace itself (i.e. you do not need to create your own colcon workspace, though it is possible to do so).

```bash
$ mkdir -p <parent-directory>
$ cd <parent-directory>
$ git clone https://github.com/westonrobot/wr_devkit_navigation.git
```

## Install Dependencies
Each sensor kit and robot base has its own set of dependencies. Please follow the instructions below to install the necessary items for your specific hardware configuration.

### Sensor Kits Dependencies
The following dependencies are specific to each sensor kit and should be installed according to the specific hardware configuration.

#### Livox Mid360 Lidar + IMU Sensor Kit
  * Livox SDK2
    ```bash
    $ cd ~
    $ git clone https://github.com/Livox-SDK/Livox-SDK2.git
    $ cd Livox-SDK2
    $ mkdir build && cd build && cmake .. && make
    $ sudo make install
    ```
    > **Note:** You can build and install the Livox-SDK2 at your preferred places other than "~/Livox-SDK2". And you can optionally remove the "Livox-SDK2" folder after installation.

### Robot Bases Dependencies
The following dependencies are specific to each robot base and should be installed according to the specific hardware configuration.

#### Ranger Mini 2.0 & Scout Mini
* ugv_sdk dependencies
  ```bash
  sudo apt-get install build-essential git cmake libasio-dev
  ```

### ROS Driver Packages
All ROS driver packages are listed in the [navigation.repos](/navigation.repos) file. You can import the ROS driver packages by running the following command:
  ```bash
  $ vcs import --recursive src < ./navigation.repos
  ```

## Build the Workspace

After installing the dependencies, you can build the workspace by running the following commands:
```bash
$ cd <parent-directory>/wr_devkit_navigation
$ source /opt/ros/humble/setup.bash
$ colcon build --symlink-install
```
