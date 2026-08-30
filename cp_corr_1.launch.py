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
                "0.430779",
                "--y",
                "0.740722",
                "--z",
                "0.550364",
                "--qx",
                "-0.285854",
                "--qy",
                "-0.114417",
                "--qz",
                "0.887148",
                "--qw",
                "-0.343751",
                # "--roll",
                # "0.458044",
                # "--pitch",
                # "-0.442863",
                # "--yaw",
                # "-2.2974",
            ],
        ),
    ]
    return LaunchDescription(nodes)
