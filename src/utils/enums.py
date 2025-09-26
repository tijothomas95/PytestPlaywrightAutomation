from enum import Enum


class Browser(Enum):
    CHROMIUM = 'chromium'
    FIREFOX = 'firefox'


class TravelType(Enum):
    RETURN_TRIP = 'Return trip'
    ONE_WAY = 'One way'

    def __str__(self):
        return self.value

class Location(Enum):
    DUBLIN = 'Dublin'
    MADRID = 'Madrid'

    def __str__(self):
        return self.value


class PassengerType(Enum):
    ADULTS = 'Adults'
    TEENS = 'Teens'
    CHILDREN = 'Children'
    INFANT = 'Infant'

    def __str__(self):
        return self.value


class FareType(Enum):
    BASIC = 'Basic'
    REGULAR = 'Regular'
    PLUS = 'Plus'
    FLEXI_PLUS = 'Flexi Plus'

    def __str__(self):
        return self.value
