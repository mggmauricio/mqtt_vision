from setuptools import setup, find_packages

setup(
    name="mqtt_vision",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",
        "protobuf",
    ],
    entry_points={
        "console_scripts": [
            "mqtt-vision=udp_receiver:main",  # Altere conforme necessário
        ],
    },
    description="A package for handling MQTT communication for vision data.",
    author="Mauricio Godoy",
    author_email="mauricio.godoy@acad.ufsm.br",
    url="https://github.com/nggmauricio/mqtt_vision",  # Altere para o URL do seu repositório
)
