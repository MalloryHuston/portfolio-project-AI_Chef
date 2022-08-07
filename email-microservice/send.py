#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='email')

channel.basic_publish(exchange='', routing_key='email', body='yes')
print(" [x] Preparing email for launch!")
connection.close()
