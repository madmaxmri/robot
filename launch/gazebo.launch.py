import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

import xacro


def generate_launch_description():

    pkg_robot = get_package_share_directory("robot")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    world = os.path.join(
        pkg_robot,
        "worlds",
        "empty.sdf"
    )

    xacro_file = os.path.join(
        pkg_robot,
        "description",
        "robot.urdf.xacro"
    )

    robot_description = xacro.process_file(xacro_file).toxml()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": f"-r {world}"
        }.items()
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": True
        }],
        output="screen"
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-world", "empty",
            "-topic", "robot_description",
            "-name", "robot",
            "-x", "0",
            "-y", "0",
            "-z", "0.2"
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])