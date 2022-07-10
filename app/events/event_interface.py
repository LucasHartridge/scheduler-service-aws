from abc import ABC, abstractmethod


class EventInterface(ABC):
    @abstractmethod
    def dispatch(self):
        """ Abstract dispatch method for Events. """
