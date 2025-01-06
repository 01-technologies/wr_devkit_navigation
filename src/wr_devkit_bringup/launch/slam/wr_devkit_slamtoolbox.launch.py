from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Define launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation (Gazebo) clock if true",
    )

    declare_params_file_cmd = DeclareLaunchArgument(
        "params_file",
        default_value=PathJoinSubstitution([
            FindPackageShare("slam_toolbox"),
            "config",
            "mapper_params_online_async.yaml"
        ]),
        description="Full path to the parameters file to use for the SLAM toolbox node",
    )

    declare_map_yaml_cmd = DeclareLaunchArgument(
        "map", 
        default_value="",
        description="Full path to map yaml file to load"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")
    map_yaml_file = LaunchConfiguration("map")

    # Node to launch SLAM toolbox
    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[params_file, {"use_sim_time": use_sim_time}],
        remappings=[("/scan", "/scan")],
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_params_file_cmd,
        declare_map_yaml_cmd,
        slam_toolbox_node
    ])
