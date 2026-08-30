import time
import json
import cv2
import threading
from pathlib import Path
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.77.23"
WAYPOINTS_FILE = Path("sweep_waypoints.json")
OUTPUT_DIR = Path("overlay_dataset_2026-07")

class CameraCacheNode(Node):
    def __init__(self):
        super().__init__('camera_cache_node')
        self.bridge = CvBridge()
        self.latest_images = {"camera_1": None, "camera_2": None}
        
        self.create_subscription(Image, '/camera_1/color/image_raw', self.cam1_cb, 10)
        self.create_subscription(Image, '/camera_2/color/image_raw', self.cam2_cb, 10)

    def cam1_cb(self, msg): 
        self.latest_images["camera_1"] = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
    def cam2_cb(self, msg): 
        self.latest_images["camera_2"] = self.bridge.imgmsg_to_cv2(msg, "bgr8")

def main():
    # 1. Load waypoints
    if not WAYPOINTS_FILE.exists():
        print(f"Error: {WAYPOINTS_FILE} not found. Run record_waypoints.py first.")
        return
        
    with open(WAYPOINTS_FILE, "r") as f:
        data = json.load(f)
        waypoints = data.get("waypoints", [])
        
    if not waypoints:
        print(f"Error: No waypoints found in {WAYPOINTS_FILE}.")
        return
        
    print(f"Loaded {len(waypoints)} waypoints from {WAYPOINTS_FILE}.")

    # 2. Init ROS 2 camera listener in background
    rclpy.init()
    cam_node = CameraCacheNode()
    executor_thread = threading.Thread(target=rclpy.spin, args=(cam_node,), daemon=True)
    executor_thread.start()

    # 3. Connect to robot RTDE
    print(f"Connecting to robot at {ROBOT_IP}...")
    try:
        rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
        rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
    except Exception as e:
        print(f"Error connecting to robot: {e}")
        rclpy.shutdown()
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    
    print("Starting sweep...")
    try:
        for i, joints in enumerate(waypoints):
            print(f"\nMoving to waypoint {i+1}/{len(waypoints)}...")
            # Command joint movement (moveJ)
            rtde_c.moveJ(joints, speed=0.4, acceleration=0.2)
            
            # Settle time is mandatory to eliminate vibration blur
            time.sleep(1.5)
            
            # Grab RTDE Ground Truth
            actual_q = rtde_r.getActualQ()
            tcp_pose = rtde_r.getActualTCPPose()
            
            # Grab latest images cached by ROS 2 subscriptions
            img1 = cam_node.latest_images["camera_1"]
            img2 = cam_node.latest_images["camera_2"]
            
            if img1 is None or img2 is None:
                print(f"Warning: Missing camera frames at waypoint {i+1}. Retrying wait...")
                time.sleep(1.0)
                img1 = cam_node.latest_images["camera_1"]
                img2 = cam_node.latest_images["camera_2"]
                if img1 is None or img2 is None:
                    print(f"Skipping save for waypoint {i+1} due to missing camera data.")
                    continue

            # Save data to disk
            prefix = OUTPUT_DIR / f"wp_{i:02d}"
            cv2.imwrite(f"{prefix}_cam1.png", img1)
            cv2.imwrite(f"{prefix}_cam2.png", img2)
            
            state_data = {
                "joint_positions": actual_q,
                "tcp_pose_rtde": tcp_pose,
                "timestamp": time.time()
            }
            with open(f"{prefix}_state.json", "w") as f:
                json.dump(state_data, f, indent=2)

            print(f"Waypoint {i+1} captured successfully.")

    finally:
        # Clean up connection
        rtde_c.stopScript()
        rclpy.shutdown()
        print("\nCapture sweep complete.")

if __name__ == '__main__':
    main()
