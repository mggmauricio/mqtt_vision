# mqtt_vision/data/__init__.py

# Este arquivo pode estar vazio ou você pode importar classes específicas
# Se você quiser expor algo do subdiretório, faça assim:
from .messages_robocup_ssl_detection_pb2 import *
from .messages_robocup_ssl_geometry_pb2 import *
from .messages_robocup_ssl_wrapper_pb2 import *

# __all__ pode ser definido aqui também, se necessário
__all__ = [
    "messages_robocup_ssl_detection_pb2",
    "messages_robocup_ssl_geometry_pb2",
    "messages_robocup_ssl_wrapper_pb2",
]
