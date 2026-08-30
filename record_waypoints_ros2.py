import json
import sys
import threading
from pathlib import Path
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

OUTPUT_FILE = Path("sweep_waypoints.json")

class WaypointRecorder(Node):
    def __init__(self):
        super().__init__('waypoint_recorder')
        self.latest_joints = None
        self.joint_names = None
        
        # Subscribe to joint states from the active driver
        self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_cb,
            10
        )

    def joint_cb(self, msg):
        # We need to map joints to the UR standard order:
        # [shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3]
        ur_order = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        if all(name in msg.name for name in ur_order):
            joint_map = dict(zip(msg.name, msg.position))
            self.latest_joints = [joint_map[name] for name in ur_order]

def main():
    rclpy.init()
    node = WaypointRecorder()
    
    # Spin in a background thread to receive joint updates
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    print("Waiting for joint states to be published...")
    while rclpy.ok() and node.latest_joints is None:
        pass
    print("Joint states detected successfully!")

    waypoints = []
    print("\n--- ROS 2 Waypoint Recording Active ---")
    print("Instructions:")
    print("  1. Move the arm to a desired waypoint (using freedrive).")
    print("  2. Press Enter in this terminal to record the current joint pose.")
    print("  3. Type 'q' and press Enter to save all waypoints and exit.")
    print("---------------------------------------")

    try:
        while True:
            user_input = input(f"Press Enter to record Waypoint {len(waypoints) + 1} (or 'q' to quit): ").strip().lower()
            if user_input == 'q':
                break
            
            # Record current joints
            q = node.latest_joints
            waypoints.append(q)
            print(f"Recorded Waypoint {len(waypoints)}: {q}")
            
    finally:
        rclpy.shutdown()

    if waypoints:
        data = {
            "waypoints": waypoints,
            "metadata": {
                "robot": "ur3e",
                "description": "8-pose workspace corner sweep for camera projection validation",
                "date_created": "2026-07-14"
            }
        }
        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nSuccessfully saved {len(waypoints)} waypoints to {OUTPUT_FILE}")
    else:
        print("\nNo waypoints recorded.")

if __name__ == '__main__':
    main()
