from launch import LaunchDescription
from launch.actions import GroupAction, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.launch_context import LaunchContext
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.utilities import perform_substitutions, normalize_to_list_of_substitutions
from typing import Dict, Text

import os
import xacro


class Xacro(Substitution):
    def __init__(self, file_path: SomeSubstitutionsType, mappings: Dict[str, SomeSubstitutionsType] = {}, verbose: bool = False):
        super().__init__()
        self.__file_path = normalize_to_list_of_substitutions(file_path)
        self.__mappings = {key: normalize_to_list_of_substitutions(value) for key, value in mappings.items()}
        self.__verbose = verbose
    
    def describe(self) -> Text:
        return f"Xacro: {self.__file_path}"

    def perform(self, context: LaunchContext) -> Text:
        file_path = perform_substitutions(context, self.__file_path)
        mappings = {key: perform_substitutions(context, value) for key, value in self.__mappings.items()}

        if self.__verbose:
            print(f"xacro file_path: {file_path}")
            print(f"xacro mappings: {mappings}")
        document = xacro.process_file(file_path, mappings=mappings)
        document_string = document.toprettyxml(indent="  ")

        if self.__verbose:
            print(f"xacro result: {document_string}")
        return document_string

def generate_launch_description():

    # --------- Arguments ---------
    front_camera = LaunchConfiguration("front_camera")
    rear_camera = LaunchConfiguration("rear_camera")
    left_camera = LaunchConfiguration("left_camera")
    right_camera = LaunchConfiguration("right_camera")

    declare_use_namespace_arg = DeclareLaunchArgument(
        "use_namespace",
        default_value="false",
        description="Whether to apply a namespace"
    )

    declare_namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Top-level namespace"
    )

    # --------- Namespace ---------
    PushRosNamespace(
        condition=IfCondition(LaunchConfiguration("use_namespace")),
        namespace=LaunchConfiguration("namespace")
    )

    # --------- Description ---------
    load_description = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="mid360_sensor_kit_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": Xacro(
                    file_path=os.path.join(
                        FindPackageShare("mid360_sensor_kit_bringup").find(
                            "mid360_sensor_kit_bringup"),
                        "urdf/sensor_kit.urdf.xacro"
                    ),
                    mappings={
                        'front_camera': front_camera,
                        'rear_camera': rear_camera,
                        'left_camera': left_camera,
                        'right_camera': right_camera
                    },
                )
            }
        ],
        remappings=[
            ("robot_description", "mid360_sensor_kit_description"),
        ]
    )

    # --------- Drivers ---------
    imu_bringup = GroupAction([
        Node(
            package="wrp_ros2",
            name="ch104m_imu_sensor_node",
            executable="imu_sensor_node",
            output="screen",
            parameters=[
                PathJoinSubstitution([
                    FindPackageShare('mid360_sensor_kit_bringup'),
                    'config',
                    'hipnuc.param.yaml'])
            ],
        )
    ])

    user_config_path = PathJoinSubstitution([
        FindPackageShare('mid360_sensor_kit_bringup'),
        "config",
        "MID360_config.json"
    ])

    lidar_bringup = GroupAction([
        Node(
            package='livox_ros_driver2',
            executable='livox_ros_driver2_node',
            name='livox_lidar_publisher',
            output='screen',
            parameters=[
                PathJoinSubstitution([
                    FindPackageShare('mid360_sensor_kit_bringup'),
                    'config',
                    'mid360.param.yaml']),
                {"user_config_path": user_config_path},
            ]
        ),
        Node(
            package="pointcloud_to_laserscan",
            executable="pointcloud_to_laserscan_node",
            name="pointcloud_to_laserscan_node",
            output="screen",
            parameters=[{
                "range_min": 0.1,
                "range_max": 100.0,
                "scan_time": 0.1,
                "min_height": -0.025,
                "max_height": 0.025,
                "angle_min": -3.14159265,
                "angle_max": 3.14159265,
                "angle_increment": 0.0174532925,
                "inf_epsilon": 1.0,
                "tf_tolerance": 0.03,
            }],
            remappings=[
                ("/cloud_in", "/livox/lidar"),
                ("/scan", "/scan"),
            ],
        ),
    ])

    # --------- Cameras ---------
    camera_type = [front_camera, rear_camera, left_camera, right_camera]
    camera_pos = ['front', 'rear', 'left', 'right']
    
    realsense_camera_bringup = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare("realsense2_camera"),
                    "launch",
                    "rs_launch.py",
                ])
            ]),
            condition=IfCondition(PythonExpression(["'", type, "' == 'realsense_d435'"])),
            launch_arguments={
                "camera_name": pos + "_d435",
                "camera_namespace": pos + "_d435",
                "config_file": PathJoinSubstitution([FindPackageShare("mid360_sensor_kit_bringup"), 'config', pos + '_d435.param.yaml'])
            }.items(),
        ) for type, pos in zip(camera_type, camera_pos)
    ])

    rgb_camera_bringup = GroupAction([
        Node(
            condition=IfCondition(PythonExpression(["'", type, "' == 'rgb_camera'"])),
            package="usb_cam",
            executable="usb_cam_node_exe",
            namespace=pos + "_rgb",
            name=pos + "_rgb",
            output="screen",
            parameters=[
                PathJoinSubstitution([FindPackageShare("mid360_sensor_kit_bringup"), 'config', 'rgb_camera.yaml'])
            ],
            remappings=[
                ('image_raw', f'{pos}_rgb/image_raw'),
                ('image_raw/compressed', f'{pos}_rgb/image_raw/compressed'),
                ('image_raw/compressedDepth', f'{pos}_rgb/image_raw/compressedDepth'),
                ('image_raw/theora', f'{pos}_rgb/image_raw/theora'),
                ('camera_info', f'{pos}_rgb/camera_info')
            ]
        ) for type, pos in zip(camera_type, camera_pos)
    ])

    return LaunchDescription([
        declare_use_namespace_arg,
        declare_namespace_arg,
        load_description,
        imu_bringup,
        lidar_bringup,
        realsense_camera_bringup,
        rgb_camera_bringup
    ])