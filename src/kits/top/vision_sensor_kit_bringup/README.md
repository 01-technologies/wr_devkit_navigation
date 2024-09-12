# Vision Sensor Kit Bringup

![Mid360 Sensor Kit](docs/vision_sensor_kit.png)

## Overview
This package contains launch and config files to launch Weston Robot's Vision Sensor Kit (top).

## Usage
To launch the Vision Sensor Kit, use the provided launch file:
```bash
ros2 launch vision_sensor_kit_bringup sensor_kit.launch.py
```

## Launch Files
* [sensor_kit.launch.py](./launch/sensor_kit.launch.py)
  * Sample launch file to launch the top sensor kit sensors with the following configuration
    * Camera model: realsense_d435i / rgb_camera

  | Argument      | Description                  | Default Value                                                                    |
  | ------------- | ---------------------------- | -------------------------------------------------------------------------------- |
  | use_namespace | Whether to apply a namespace | `False`                                                                          |
  | namespace     | Top-level namespace          | `""`                                                                             |
  | front_camera  | Front camera model           | `""`<br/> Possible values: rgb_camera, realsense_d435i<br/>Leave blank for "none" |
  | rear_camera   | Rear camera model            | `""`<br/> Possible values: rgb_camera, realsense_d435i<br/>Leave blank for "none" |
  | left_camera   | Left camera model            | `""`<br/> Possible values: rgb_camera, realsense_d435i<br/>Leave blank for "none" |
  | right_camera  | Right camera model           | `""`<br/> Possible values: rgb_camera, realsense_d435i<br/>Leave blank for "none" |

## Nodes
The package will launch the various sensors and their associated driver nodes/supporting nodes

* Description
  * Package: robot_state_publisher
  * Executable/Plugin: robot_state_publisher
  * Name: vision_sensor_kit_state_publisher
* Realsense Camera
  * Driver
    * Package: realsense2_camera
    * Launch File: rs_launch.py
    * Name: <CAMERA_POSITION>_cam/d435i
* RGB Camera
  * Driver
    * Package: usb_cam
    * Executable: usb_cam_node_exe
    * Name: <CAMERA_POSITION>_cam/rgb

## Configuration
To better suit your needs/setup, you may need to adjust these accordingly
* [Configuration files](./config/)
* [Launch files](./launch/)