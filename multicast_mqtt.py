import socket
import struct
import paho.mqtt.client as mqtt
from google.protobuf import json_format
from .data.messages_robocup_ssl_wrapper_pb2 import (
    SSL_WrapperPacket,
)  # Ajustado o import


class MulticastMQTT:
    def __init__(self, multicast_group, multicast_port, mqtt_broker, mqtt_topic):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic

        # Configuração do cliente MQTT
        self.client = mqtt.Client(
            protocol=mqtt.MQTTv311
        )  # ⚡ Trocar para MQTT v3.1.1 para evitar problemas
        self.client.on_connect = self.on_connect  # Adiciona callback de conexão
        self.client.connect(self.mqtt_broker)

        self.client.loop_start()  # ⚡ Starta o loop do MQTT

        # Configuração do socket multicast
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 🔥 Alterado para '0.0.0.0' para permitir recebimento de multicast no Docker
        self.sock.bind(("0.0.0.0", self.multicast_port))

        mreq = struct.pack(
            "4sl", socket.inet_aton(self.multicast_group), socket.INADDR_ANY
        )
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado ao MQTT Broker {self.mqtt_broker} com código: {rc}")

    def start_receiving(self):
        print(f"Escutando multicast em {self.multicast_group}:{self.multicast_port}...")
        while True:
            try:
                data, addr = self.sock.recvfrom(2048)  # Buffer de 2048 bytes
                print(f"\nRecebido de {addr}: {data.hex()}")

                wrapper_packet = SSL_WrapperPacket()
                wrapper_packet.ParseFromString(data)  # Decodificando o Protobuf

                # Publicando os dados de detecção
                if wrapper_packet.HasField("detection"):
                    detection_json = json_format.MessageToJson(wrapper_packet.detection)
                    self.client.publish(f"{self.mqtt_topic}/detection", detection_json)
                    print(f"Publicado dados de detecção: {detection_json}")

                # Publicando os dados de geometria
                if wrapper_packet.HasField("geometry"):
                    geometry_json = json_format.MessageToJson(wrapper_packet.geometry)
                    self.client.publish(f"{self.mqtt_topic}/geometry", geometry_json)
                    print(f"Publicado dados de geometria: {geometry_json}")

            except Exception as e:
                print(f"Erro ao processar dados: {e}")


if __name__ == "__main__":
    multicast_group = "224.5.23.2"
    multicast_port = 10020
    mqtt_broker = "mqtt"  # Nome do serviço do broker MQTT no docker-compose
    mqtt_topic = "seu/topico"

    multicast_mqtt = MulticastMQTT(
        multicast_group, multicast_port, mqtt_broker, mqtt_topic
    )
    multicast_mqtt.start_receiving()
