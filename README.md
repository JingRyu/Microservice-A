# Age Verification Microservice
The age verification microservice handles age verification and provides educational content based on movie age restrictions. It also tracks the number of login attempts.

### Communication Contract
To request data from the Age Verification Microservice, you need to send a message to the RabbitMQ queue age_verify_queue with the following structure:

**For Age Verification:**<br />
Method: age_verification<br />
Argument: birth_year (integer)

**For Educational Content:**<br />
Method: show_educational_content<br />
No argument required

**For Login Attempts:**<br />
Method: count_login_attempts<br />
No argument required

In order to do these, you should:

1. Install Python, RabbitMQ and Pika
2. In the terminal, type "python AgeVerificationServer.py"
3. In a new terminal, type "python AgeVerificationClient.py"
4. in your program, import AgeVerificationClient and call the method you need. Use age_verification.call() to request data and waiting. The proper received data will be returned (see the following example code).

>import AgeVerificationClient<br />
>
>age_verification = AgeVerificationClient.AgeVerificationClient()<br />
>
>print(" [x] Requesting age verify(1994)")<br />
>response = age_verification.call('age_verification', 1994)<br />
>print(f" [.] Got {response}")<br />
>
>print(" [x] Requesting educational content")<br />
>response = age_verification.call('show_educational_content')<br />
>print(f" [.] Got {response}")<br />
>    
>print(" [x] Requesting login attempts")<br />
>response = age_verification.call('count_login_attempts')<br />
>print(f" [.] Got {response}")<br />


![9BBF3DE2-A080-4B16-98B0-146D127BC33D](https://github.com/JingRyu/Microservice-A/assets/81526024/f6328348-94b2-4999-b053-64b9ce74cb57)
