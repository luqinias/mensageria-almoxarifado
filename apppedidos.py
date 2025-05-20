#Jose Lucas Lira Bizil, Engenharia de Computação, 12411ECP005, Arquitetura de Software Aplicada 
# apppedidos.py
import pika
import json

def publicar_pedido(pedido):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('guest', 'guest'))
    )
    channel = connection.channel()
    
    channel.queue_declare(
        queue='fila_pedidos',
        durable=True,
        arguments={'x-queue-type': 'quorum'}  
    )
    
    channel.basic_publish(
        exchange='',
        routing_key='fila_pedidos',
        body=json.dumps(pedido),
        properties=pika.BasicProperties(
            delivery_mode=2,  
            content_type='application/json'
        )
    )

    print(f"Pedido {pedido['id']} publicado")
    connection.close()


novo_pedido = {
    "id": "87639",
    "produto": "prego",
    "quantidade": 5,
    "status": "enviado_almoxarifado"
    }

publicar_pedido(novo_pedido)
