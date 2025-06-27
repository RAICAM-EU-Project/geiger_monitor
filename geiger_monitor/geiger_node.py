import rclpy
from rclpy.node import Node
from marti_common_msgs.msg import Float32Stamped
import smbus
import struct
import time

class GeigerI2CNode(Node):
    def __init__(self):
        super().__init__('geiger_i2c_node')
        self.publisher_ = self.create_publisher(Float32Stamped, 'radiation_level', 10)
        self.bus = smbus.SMBus(1)  # Use correct I2C bus for Orin NX
        self.address = 0x08
        self.timer = self.create_timer(1.0, self.read_and_publish)

    def read_and_publish(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, 0, 4)
            value = struct.unpack('f', bytes(data))[0]
            msg = Float32Stamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "geiger_sensor"
            msg.value = value
            self.publisher_.publish(msg)
            self.get_logger().info(f'I2C Radiation: {value:.3f} uSv/h')
        except Exception as e:
            self.get_logger().error(f'I2C Read failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = GeigerI2CNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
