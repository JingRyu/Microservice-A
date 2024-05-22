# server
import pika
from datetime import datetime
import textwrap
import ast

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='age_verify_queue')

# Global variable for login attempts
login_attempts = 0

def age_verification(birth_year):
    global login_attempts
    login_attempts += 1
    current_year = datetime.now().year
    return (int(current_year) - int(birth_year)) >= 18

def show_educational_content():
    content = ("Age restrictions for movies ensure content appropriateness for different age groups, "
               "protecting younger audiences from unsuitable material. They help parents make informed "
               "decisions about what their children watch by providing guidelines on language, violence, "
               "sexual content, and other sensitive themes. These restrictions comply with legal regulations "
               "and uphold industry standards to prevent exposure to harmful content. Rating systems like MPAA "
               "(G, PG, PG-13, R, NC-17) and BBFC (U, PG, 12A, 15, 18) guide viewers on content suitability, "
               "promoting a safe and responsible media consumption experience for all ages.")

    wrapped_content = textwrap.fill(content, width=70)
    return wrapped_content

def count_login_attempts():
    global login_attempts
    return login_attempts

def on_request(ch, method, props, body):
    message = ast.literal_eval(body.decode('utf-8'))
    method_name = message['method']
    arg = message.get('arg')

    print(f" [.] {method_name}({arg})")
    if method_name == 'age_verification':
        response = age_verification(int(arg))
        print(f" [.] Total login attempts: {login_attempts}")
    elif method_name == 'show_educational_content':
        response = show_educational_content()
    elif method_name == 'count_login_attempts':
        response = count_login_attempts()
    else:
        response = 'Unknown method'

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='age_verify_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
