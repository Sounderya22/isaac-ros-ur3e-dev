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
                "0.426236",
                "--y",
                "0.746044",
                "--z",
                "0.54932",
                "--qx",
                "-0.285876",
                "--qy",
                "-0.110277",
                "--qz",
                "0.886734",
                "--qw",
                "-0.346145",
                # "--roll",
                # "0.451128",
                # "--pitch",
                # "-0.445212",
                # "--yaw",
                # "-2.29347",
            ],
        ),
    ]
    return LaunchDescription(nodes)
