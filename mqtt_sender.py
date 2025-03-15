import paho.mqtt.client as mqtt
import json


class MQTTSender:
    """
    A base class for sending messages via MQTT.

    Attributes:
        broker (str): The MQTT broker address.
        port (int): The port to connect to the MQTT broker.
        client (mqtt.Client): The MQTT client instance.
    """

    def __init__(self, broker: str, port: int):
        """
        Initializes the MQTTSender with the specified broker and port.

        Args:
            broker (str): The MQTT broker address.
            port (int): The port to connect to the MQTT broker.
        """
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.connect()  # Connect once during initialization

    def connect(self):
        """Connects to the MQTT broker."""
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()  # Start the loop to process network traffic

    def disconnect(self):
        """Disconnects from the MQTT broker."""
        self.client.loop_stop()  # Stop the loop
        self.client.disconnect()

    def publish(self, topic: str, payload: str):
        """
        Publishes a message to the specified MQTT topic.

        Args:
            topic (str): The topic to publish the message to.
            payload (str): The message payload in JSON format.

        Raises:
            JSONDecodeError: If the payload cannot be decoded as JSON.
        """
        # Convert the string JSON into a dictionary
        try:
            json_payload = json.loads(payload)
        except json.JSONDecodeError:
            print("Error decoding JSON string.")
            return

        # Publish the dictionary as JSON
        self.client.publish(topic, json.dumps(json_payload))
