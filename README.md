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

1. In the terminal, type "python AgeVerificationServer.py"
2. In a new terminal, type "python AgeVerificationClient.py"
3. in your program, import AgeVerificationClient and call the method you need.

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
