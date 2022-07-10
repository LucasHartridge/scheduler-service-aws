import boto3

from app.config import config
from botocore.exceptions import ClientError
from app.events.event_interface import EventInterface


class Notification(EventInterface):
    def __init__(self, data):
        self.subscriber = data["subscriber"]
        self.coins_price = data["coins_price"]

    def __repr__(self):
        """Representation of ScheduledEvent
        :return: string
        """
        return f"<NotificationEvent, subscriber={self.subscriber}, coins_price={self.coins_price}"

    def dispatch(self):
        try:
            client = boto3.client("ses",
                                  aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                  aws_session_token=config.AWS_SESSION_TOKEN,
                                  endpoint_url=config.SCHEDULER_SERVICE_URL,
                                  region_name=config.AWS_DEFAULT_REGION)

            response = client.send_email(
                Destination=dict(
                    ToAddresses=[self.subscriber]),
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': f'''
                                    <!DOCTYPE html>
                                    <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang=en>
                                        Here should be the defined the template of the email. This will not be covered on this example
                                        {self.coins_price}
                                    </html>
                                    ''',
                        },
                        'Text': {
                            'Charset': "UTF-8",
                            'Data': "Email Sent by Lucas"
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': "Showing how is possible to create a scheduler service with AWS",
                    },
                },
                Source="Lucas Medium <lucas-medium@gmail.com>"
            )

            return {"statusCode": 200, "body": f"Notification Sent. MessageId: {response['MessageId']}"}
        except ClientError as e:
            return {"statusCode": 500, "body": e.response['Error']['Message']}
