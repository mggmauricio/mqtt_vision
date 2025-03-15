import socket
import json
import paho.mqtt.client as mqtt
from data import messages_robocup_ssl_wrapper_pb2 as ssl_wrapper


class UDPReceiver:
    def __init__(self, multicast_group: str, port: int, mqtt_broker: str):
        self.multicast_group = multicast_group
        self.port = port
        self.mqtt_broker = mqtt_broker
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.bind(("", self.port))

        # Join the multicast group
        group = socket.inet_aton(self.multicast_group)
        mreq = group + socket.inet_aton("0.0.0.0")
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Setup MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(self.mqtt_broker)

    def listen(self):
        print(f"Listening for messages on {self.multicast_group}:{self.port}")
        while True:
            data, _ = self.sock.recvfrom(1024)  # Buffer size of 1024 bytes
            self.process_message(data)

    def process_message(self, data):
        wrapper_packet = ssl_wrapper.SSL_WrapperPacket()
        if wrapper_packet.ParseFromString(data):
            # Prepare the data to send to MQTT
            vision_data = {
                "frame_number": wrapper_packet.detection.frame_number,
                "timestamp": wrapper_packet.detection.t_capture,
                "balls": [
                    {
                        "confidence": ball.confidence,
                        "x": ball.x,
                        "y": ball.y,
                    }
                    for ball in wrapper_packet.detection.balls
                ],
                "robots_yellow": [
                    {
                        "robot_id": robot.robot_id,
                        "confidence": robot.confidence,
                        "x": robot.x,
                        "y": robot.y,
                    }
                    for robot in wrapper_packet.detection.robots_yellow
                ],
                "robots_blue": [
                    {
                        "robot_id": robot.robot_id,
                        "confidence": robot.confidence,
                        "x": robot.x,
                        "y": robot.y,
                    }
                    for robot in wrapper_packet.detection.robots_blue
                ],
            }
            # Publish the vision data to MQTT
            self.mqtt_client.publish("vision/data", json.dumps(vision_data))
        else:
            print("Received an invalid SSL_WrapperPacket")


# Example usage
if __name__ == "__main__":
    receiver = UDPReceiver(
        multicast_group="224.5.23.2", port=10006, mqtt_broker="localhost"
    )
    receiver.listen()
