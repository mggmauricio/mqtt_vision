from mqtt_sender import MQTTSender
from data import messages_robocup_ssl_wrapper_pb2 as ssl_wrapper
import json


class VisionSender(MQTTSender):
    """A class for sending vision data via MQTT."""

    VISION_TOPIC = "vision/data"

    def send_vision_data(self, vision_frame: ssl_wrapper.SSL_DetectionFrame):
        """
        Sends vision data to the MQTT broker.

        Args:
            vision_frame (SSL_DetectionFrame): The vision data to send.
        """
        # Convert the vision object to a JSON string
        vision_data = {
            "frame_number": vision_frame.frame_number,
            "timestamp": vision_frame.t_capture,
            "balls": [
                {
                    "confidence": ball.confidence,
                    "x": ball.x,
                    "y": ball.y,
                    "pixel_x": ball.pixel_x,
                    "pixel_y": ball.pixel_y,
                }
                for ball in vision_frame.balls
            ],
            "robots_yellow": [
                {
                    "robot_id": robot.robot_id,
                    "confidence": robot.confidence,
                    "x": robot.x,
                    "y": robot.y,
                    "orientation": robot.orientation,
                    "pixel_x": robot.pixel_x,
                    "pixel_y": robot.pixel_y,
                }
                for robot in vision_frame.robots_yellow
            ],
            "robots_blue": [
                {
                    "robot_id": robot.robot_id,
                    "confidence": robot.confidence,
                    "x": robot.x,
                    "y": robot.y,
                    "orientation": robot.orientation,
                    "pixel_x": robot.pixel_x,
                    "pixel_y": robot.pixel_y,
                }
                for robot in vision_frame.robots_blue
            ],
        }
        self.publish(self.VISION_TOPIC, json.dumps(vision_data))
