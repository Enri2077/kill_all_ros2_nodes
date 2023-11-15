#!/usr/bin/python3

from ros2node.api import get_node_names
import rclpy
import psutil
import time


rclpy.init()
this_node_name = "list_nodes"
this_node = rclpy.create_node(this_node_name)

rclpy.spin_once(this_node, timeout_sec=1.0)
rclpy.spin_once(this_node, timeout_sec=1.0)

def list_nodes():
    available_nodes = get_node_names(node=this_node, include_hidden_nodes=False)
    ros2_node_name_list = list()
    print("ROS2 NODES:")
    for name, namespace, full_name in available_nodes:
        if name == this_node_name:
            continue
        ros2_node_name_list.append(name)
        print(f"\t- {name} (namespace: {namespace}, full name: {full_name})")
    return ros2_node_name_list


ros2_node_names = list_nodes()
for proc in psutil.process_iter():
    for ros2_node_name in ros2_node_names:
        if f"__node:={ros2_node_name}" in proc.cmdline() or ros2_node_name in proc.name():
            print(f"sending kill signal to {proc.name()}")
            proc.kill()

rclpy.spin_once(this_node, timeout_sec=1.0)
rclpy.spin_once(this_node, timeout_sec=1.0)
list_nodes()

this_node.destroy_node()
rclpy.shutdown()

