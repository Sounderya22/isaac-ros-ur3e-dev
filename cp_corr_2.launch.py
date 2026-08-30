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
                "0.434988",
                "--y",
                "0.747898",
                "--z",
                "0.543758",
                "--qx",
                "-0.284947",
                "--qy",
                "-0.116572",
                "--qz",
                "0.888105",
                "--qw",
                "-0.341299",
                # "--roll",
                # "0.460032",
                # "--pitch",
                # "-0.440679",
                # "--yaw",
                # "-2.303",
            ],
        ),
    ]
    return LaunchDescription(nodes)
