import logging

from app.events.event import Event

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        event = Event(event=event['detail-type'], data=event)
        logger.info(
            f"Function Name: {lambda_handler.__name__}. Event: {event.kind.value}")
        return event.dispatch()
    except Exception as error:
        logger.error(
            f"Function Name: {lambda_handler.__name__}. Error: {str(error)}")
        return {"statusCode": 500, "body": str(error)}
