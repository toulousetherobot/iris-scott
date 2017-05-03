#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

payload = {
	"title": "Limit Switch Hit",
	# "type": "info",
	# "type": "success",
	# "type": "warning",
	"type": "error",
	"footnote": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
	}

channel.queue_declare(queue="messages")

print(" [x] Sent Notification")
if not channel.basic_publish(
	exchange="toulouse", routing_key="moulinrouge", body=json.dumps(payload), 
	properties=pika.BasicProperties(
		content_type='text/plain', 
		app_id="python",
		delivery_mode=1)):
	print('     Delivery not confirmed')
else:
	print('     Confirmed delivery')

connection.close()
