# mqtt_vision

`mqtt_vision` é um pacote Python para gerenciar a comunicação MQTT para dados de visão. Este pacote permite que você receba dados de visão via UDP e os publique em um broker MQTT, facilitando a integração com aplicações de robótica e sistemas de visão computacional.

## Instalação

Você pode instalar o pacote diretamente do GitHub usando o seguinte comando:

```bash
pip install git+https://github.com/mggmauricio/mqtt_vision.git
```


## Estrutura do Pacote

A estrutura do pacote é a seguinte:


```bash
mqtt_vision/
├── init.py
├── mqtt_sender.py
├── udp_receiver.py
├── requirements.txt
└── proto/
├── messages_robocup_ssl_wrapper_pb2.py
└── messages_robocup_ssl_geometry_pb2.py
```

- **mqtt_sender.py**: Classe para gerenciar a conexão MQTT e publicar mensagens.
- **udp_receiver.py**: Classe para receber mensagens UDP e processá-las.
- **proto/**: Contém arquivos gerados do Protobuf para a comunicação de dados.

## Uso

Aqui está um exemplo básico de como usar o pacote:

```python
from mqtt_vision.mqtt_sender import MQTTSender
from mqtt_vision.udp_receiver import UDPReceiver

# Inicializa o sender e receiver
mqtt_sender = MQTTSender()
udp_receiver = UDPReceiver()

# Inicia o receiver em um loop
udp_receiver.listen()
```

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir um problema ou enviar um pull request.

## Contato

Para mais informações, entre em contato com [mauricio.godoy@acad.ufsm.br](mailto:mauricio.godoy@acad.ufsm.br).