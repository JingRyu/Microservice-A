# Age Verification Microservice
The age verification microservice handles age verification and provides educational content based on movie age restrictions. It also tracks the number of login attempts.

### Communication Contract

**For Age Verification:**<br />
Method: age_verification<br />
Argument: birth_year (integer)

**For Educational Content:**<br />
Method: show_educational_content<br />
No argument required

**For Login Attempts:**<br />
Method: count_login_attempts<br />
No argument required

###To request data from the Age Verification Microservice, you should:

1. Install RabbitMQ and Pika
2. Set Up the Requesting Program that connected to the same rabbitmq queue, and create a class with a 'call' method to send requests.
3. Example Client Class:
```
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


if __name__ == "__main__":

    age_verification = AgeVerificationClient()

    print(" [x] Requesting age verify(1994)")
    response = age_verification.call('age_verification', 1994)
    print(f" [.] Got {response}")

    print(" [x] Requesting educational content")
    response = age_verification.call('show_educational_content')
    print(f" [.] Got {response}")

    print(" [x] Requesting login attempts")
    response = age_verification.call('count_login_attempts')
    print(f" [.] Got {response}")
```
###To receive data from the Age Verification Microservice, the responses are based on the method called:
For age_verification, it returns True or False.<br />
For show_educational_content, it returns a string with educational content.<br />
For count_login_attempts, it returns the number of login attempts.<br />

![9BBF3DE2-A080-4B16-98B0-146D127BC33D](https://github.com/JingRyu/Microservice-A/assets/81526024/f6328348-94b2-4999-b053-64b9ce74cb57)
