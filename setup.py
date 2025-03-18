from setuptools import setup, find_packages

setup(
    name="mqtt_multicast",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",
    ],
    description="A library to receive multicast data and send it via MQTT.",
    author="Mauricio Godoy",
    author_email="mauricio.godoy@acad.ufsm.br",
    url="https://github.com/mggmauricio/mqtt_vision",  # Altere para o seu repositório
)
