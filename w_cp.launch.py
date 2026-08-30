""" Static transform publisher acquired via MoveIt 2 hand-eye calibration """
""" EYE-IN-HAND: wrist_3_link -> camera_1_link """
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
                "wrist_3_link",
                "--child-frame-id",
                "camera_1_link",
                "--x",
                "0.0165093",
                "--y",
                "-0.061307",
                "--z",
                "0.0544068",
                "--qx",
                "0.327738",
                "--qy",
                "-0.327114",
                "--qz",
                "0.652723",
                "--qw",
                "0.599615",
                # "--roll",
                # "0.962427",
                # "--pitch",
                # "0.0355659",
                # "--yaw",
                # "1.63699",
            ],
        ),
    ]
    return LaunchDescription(nodes)
