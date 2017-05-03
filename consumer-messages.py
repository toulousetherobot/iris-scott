import pika

def on_message(channel, method_frame, header_frame, body):
    print("Message body", body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

credentials = pika.PlainCredentials('guest', 'guest')
parameters =  pika.ConnectionParameters('localhost', credentials=credentials)

print(parameters)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(exchange="toulouse", exchange_type="direct", passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue="notifications", auto_delete=True)
channel.queue_bind(queue="notifications", exchange="toulouse", routing_key="toulouse.messages")
channel.basic_qos(prefetch_count=1)

channel.basic_consume(on_message, "notifications")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()