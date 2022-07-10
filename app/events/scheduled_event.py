import json
import requests
import boto3
import logging

from app.config import config
from app.enums.event_type import EventType
from app.events.event_interface import EventInterface

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Scheduled(EventInterface):
    def __init__(self, data):
        self.time = data['time']
        self.headers = {'X-CoinAPI-Key': config.COIN_API_KEY,
                        'Content-type': 'application/json'}

    def __repr__(self):
        """Representation of Scheduled
        :return: string
        """
        return f"<Scheduled event, time={self.time}>"

    def dispatch(self):
        subscribers = self.__get_subscribers()
        coins_price = self.__get_price()

        for subscriber in subscribers:
            self.__send_notification(subscriber, coins_price)

    def __get_price(self):
        '''This function will get the price of 5 coins from the COIN API
        At the moment this is harcoded but the list of coins can be get from the user preferences'''
        response = requests.get(
            url=f"{config.COIN_API_URL}?filter_asset_id=BTC;ETC;ADA;APE;LTC",
            headers=self.headers
        )
        coins_price = [dict(id=coin["asset_id"], name=coin["name"], price_usd=coin[
                            "price_usd"]) for coin in response.json()]

        return coins_price

    def __get_subscribers(self):
        '''This function will mock a list of subscribers that want to receive the price of the coins
        This easily can be transformed into a call to an API to get this data'''
        return ["subscriber1@gmail.com", "subscriber2@gmail.com"]

    def __send_notification(self, subscriber, coins_price):
        try:
            event_payload = dict()
            event_payload['detail-type'] = EventType.NOTIFICATION.value
            event_payload['coins_price'] = coins_price
            event_payload["subscriber"] = subscriber

            client = boto3.client("lambda",
                                  aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                  aws_session_token=config.AWS_SESSION_TOKEN,
                                  endpoint_url=config.SCHEDULER_SERVICE_URL,
                                  region_name=config.AWS_DEFAULT_REGION)

            client.invoke(
                FunctionName=config.FUNCTION_NAME,
                InvocationType='Event',
                LogType='None',
                Payload=json.dumps(event_payload)
            )
        except Exception as error:
            logger.error(
                f"Function Name: {Scheduled.__name__}.{self.__send_notification.__name__}. Error: {str(error)}")
