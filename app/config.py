import os


class Config(object):
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', None)
    AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN', None)
    FUNCTION_NAME = os.getenv('FUNCTION_NAME', None)
    COIN_API_KEY = os.getenv('COIN_API_KEY', None)
    COIN_API_URL = os.getenv('COIN_API_URL', None)
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', None)
    SCHEDULER_SERVICE_URL = os.getenv('SCHEDULER_SERVICE_URL', None)


config = Config()
