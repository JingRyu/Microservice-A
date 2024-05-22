# client
import pika
import uuid


class AgeVerificationClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, method, arg=None):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = {
            'method': method,
            'arg': arg
        }
        self.channel.basic_publish(
            exchange='',
            routing_key='age_verify_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(message))
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response.decode('utf-8')


age_verification = AgeVerificationClient()

# Request age verification
print(" [x] Requesting age verify(1994)")
response = age_verification.call('age_verification', 1994)
print(f" [.] Got {response}")

# Request educational content
print(" [x] Requesting educational content")
response = age_verification.call('show_educational_content')
print(f" [.] Got {response}")

# Request login attempts
print(" [x] Requesting login attempts")
response = age_verification.call('count_login_attempts')
print(f" [.] Got {response}")
