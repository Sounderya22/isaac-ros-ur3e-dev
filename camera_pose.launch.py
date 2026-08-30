""" Static transform publisher acquired via MoveIt 2 hand-eye calibration """
""" EYE-TO-HAND: world -> camera_1_link """
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    nodes = [
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            output="log",
            arguments=[
                "--frame-id",
                "world",
                "--child-frame-id",
                "camera_1_link",
                "--x",
                "0.435213",
                "--y",
                "0.74907",
                "--z",
                "0.541034",
                "--qx",
                "-0.286693",
                "--qy",
                "-0.103783",
                "--qz",
                "0.887775",
                "--qw",
                "-0.344806",
                # "--roll",
                # "0.438721",
                # "--pitch",
                # "-0.452782",
                # "--yaw",
                # "-2.29805",
            ],
        ),
    ]
    return LaunchDescription(nodes)
