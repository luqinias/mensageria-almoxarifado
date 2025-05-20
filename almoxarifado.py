#Jose Lucas Lira Bizil, Engenharia de Computação, 12411ECP005, Arquitetura de Software Aplicada 
# appalmoxarifado.py
import pika
import json
import time

def processar_pedido():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('guest', 'guest'))
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='fila_pedidos', durable=True, arguments={'x-queue-type': 'quorum'} )
    channel.queue_declare(queue='fila_processados', durable=True)
    
    channel.basic_qos(prefetch_count=1)
    
    def callback(ch, method, properties, body):
        pedido = json.loads(body)
        print(f"Processando pedido {pedido['id']}...")
        
        time.sleep(2)
        
        pedido['status'] = "processado_almoxarifado"
        

        ch.basic_publish(
            exchange='',
            routing_key='fila_processados',
            body=json.dumps(pedido),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Pedido {pedido['id']} processado")
    
    channel.basic_consume(
        queue='fila_pedidos',
        on_message_callback=callback,
        auto_ack=False
    )
    
    print("Aguardando pedidos...")
    channel.start_consuming()

if __name__ == '__main__':
    processar_pedido()