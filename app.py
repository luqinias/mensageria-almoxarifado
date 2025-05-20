import json
import pika
from apppedidos import publicar_pedido

novo_pedido = {
    "id": "87639",
    "produto": "prego",
    "quantidade": 5,
    "status": "enviado_almoxarifado"
}

publicar_pedido(novo_pedido)