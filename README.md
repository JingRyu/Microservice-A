## Age Verification Microservice
The age verification microservice handles age verification and provides educational content based on movie age restrictions. It also tracks the number of login attempts.

# Communication Contract
To request data from the Age Verification Microservice, you need to send a message to the RabbitMQ queue age_verify_queue with the following structure:

For Age Verification:
Method: age_verification
Argument: birth_year (integer)

For Educational Content:
Method: show_educational_content
No argument required

For Login Attempts:
Method: count_login_attempts
No argument required
