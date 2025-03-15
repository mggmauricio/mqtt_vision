from mqtt_sender import MQTTSender
from data import messages_robocup_ssl_geometry_pb2 as ssl_geometry
import json


class GeometrySender(MQTTSender):
    """A class for sending geometry data via MQTT."""

    GEOMETRY_TOPIC = "geometry/data"

    def send_geometry_data(self, geometry_data: ssl_geometry.SSL_GeometryData) -> None:
        """
        Sends geometry data to the MQTT broker.

        Args:
            geometry_data (ssl_geometry.SSL_GeometryData): The geometry data to send.
        """
        # Convert the geometry object to a JSON string
        geometry = {
            "field_width": geometry_data.field_width,
            "field_height": geometry_data.field_height,
            "goal_width": geometry_data.goal_width,
            "goal_depth": geometry_data.goal_depth,
            # Add other fields as necessary
        }
        self.publish(self.GEOMETRY_TOPIC, json.dumps(geometry))  # Send as JSON string
