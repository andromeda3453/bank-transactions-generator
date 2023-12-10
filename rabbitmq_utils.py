import pika

def connection(): 
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials, port=5672, virtual_host='/'))
    channel = connection.channel()
    print('[*] Connection established to RabbitMQ server')
    return channel