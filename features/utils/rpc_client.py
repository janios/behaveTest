import pika
import time
import uuid


class RpcClient(object):

    def __init__(self, rabbit_username, rabbit_password, rabbit_hostname, rabbit_port):
        print(" --- Init RpcClient  --- ")
        print(" --- Connecting to rabbit host --> %s" % rabbit_hostname)
        print(" --- Establish RPC Client Configuration --- ")
        amq_url = "amqps://%s:%s@%s:%s/" % (rabbit_username, rabbit_password, rabbit_hostname, rabbit_port)
        self.connection = pika.BlockingConnection(
            pika.URLParameters(amq_url))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, request, queue_name):
        print(" --- Sending payload message --> %s" % request)
        start_time = time.time()
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                content_type='application/json',
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(request))
        while self.response is None:
            self.connection.process_data_events()
        print(" --- Response payload message -->  %s" % self.response)
        print(" --- RPC processed request in %s seconds ---" % (time.time() - start_time))
        return self.response
