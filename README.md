# Building a Scheduler Service with AWS and test it using Localstack

## How to run the project locally?

1. Create a Virtual Environment

```sh
$ virtualenv $VIRTUAL_ENV_NAME --python=3.8
```

2. Activate Virtual Environment

```sh
$ source ~/path/to/created/$VIRTUAL_ENV_NAME/bin/activate
```

3. Install dependencies
```sh
$ pip install -r requirements.txt
```

4. Create the .env file based on the .env.example file

5. Generate a COIN API Key for testing purposes using the following [link](https://www.coinapi.io/pricing?apikey) 

6. Run 
```sh
$ make setup
```

> In the terminal you will start seeing that the lambda is deployed and is call, executing first the Scheduled Event and finally the Notification Event. Every minute the lambda will be called again

