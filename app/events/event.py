from app.enums.event_type import EventType
from app.events.event_interface import EventInterface
from app.events.notification_event import Notification
from app.events.scheduled_event import Scheduled


class Event(EventInterface):
    def __init__(self, event, data):
        self.kind = event
        self.data = data

    def __repr__(self):
        """Representation of Event
        :return: string
        """
        return f"<Event, kind={self.kind}, data={self.data}>"

    @property
    def kind(self):
        return self.__kind

    @kind.setter
    def kind(self, event):
        if event == EventType.SCHEDULED.value:
            self.__kind = EventType.SCHEDULED
        elif event == EventType.NOTIFICATION.value:
            self.__kind = EventType.NOTIFICATION
        else:
            raise Exception('Event kind not supported')

    def dispatch(self):
        if self.kind == EventType.SCHEDULED:
            return Scheduled(self.data).dispatch()
        elif self.kind == EventType.NOTIFICATION:
            return Notification(self.data).dispatch()
