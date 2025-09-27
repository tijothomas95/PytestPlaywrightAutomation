import random
import re

from enum import Enum
from faker import Faker
from utils.enums import PassengerType
from datetime import datetime, timedelta

faker = Faker()

class Title(Enum):
    MR = "Mr"
    MRS = "Mrs"
    MS = "Ms"
    MX = "Mx"

class FakePassenger:
    def __init__(self, passenger_type: PassengerType, index: int = 0):
        if passenger_type == PassengerType.TEENS:
            dob = faker.date_of_birth(minimum_age=12, maximum_age=17)
            title = random.choice([Title.MR, Title.MS, Title.MX]).value
            form_passenger_type = "Teen"
        elif passenger_type == PassengerType.CHILDREN:
            dob = faker.date_of_birth(minimum_age=3, maximum_age=11)
            title = random.choice([Title.MR, Title.MS]).value
            form_passenger_type = "Child"
        elif passenger_type == PassengerType.INFANT:
            dob = faker.date_of_birth(minimum_age=0, maximum_age=1)
            title = random.choice([Title.MR, Title.MS]).value
            form_passenger_type = "Infant"
        else:
            dob = faker.date_of_birth(minimum_age=18, maximum_age=90)
            title = random.choice(list(Title)).value
            form_passenger_type = "Adult"

        self.first_name = faker.first_name()
        self.last_name = faker.last_name()
        self.dob = dob.strftime("%d/%m/%Y")
        self.title = title
        self.search_passenger_type = passenger_type
        self.form_passenger_type = form_passenger_type
        self.index = index


def generate_passengers(adults=2, teens=1, children=1, infants=1):
    passengers = []
    for i in range(adults):
        passengers.append(FakePassenger(PassengerType.ADULTS, i))
    for i in range(teens):
        passengers.append(FakePassenger(PassengerType.TEENS, i))
    for i in range(children):
        passengers.append(FakePassenger(PassengerType.CHILDREN, i))
    for i in range(infants):
        passengers.append(FakePassenger(PassengerType.INFANT, i))
    sorted_passengers = sorted(passengers, key=lambda p: sort_order[p.search_passenger_type])
    return sorted_passengers


sort_order = {
    PassengerType.INFANT: 0,
    PassengerType.ADULTS: 1,
    PassengerType.CHILDREN: 2,
    PassengerType.TEENS: 3,
}


def get_trip_dates(days_from_today: int = 3, return_after_days: int = 14):
    today = datetime.today()
    outbound = today + timedelta(days=days_from_today)
    inbound = outbound + timedelta(days=return_after_days)

    # format to match "2 October 2025"
    fmt = "%-d %B %Y"
    return outbound.strftime(fmt), inbound.strftime(fmt)

def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00A0", " ")).strip()