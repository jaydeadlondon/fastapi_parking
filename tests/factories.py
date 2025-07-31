import random

import factory
from faker import Faker

from module_30_ci_linters.homework.hw1.fastapi_parking.app.models import Client, Parking

fake = Faker("ru_RU")


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.LazyAttribute(lambda x: fake.first_name())
    surname = factory.LazyAttribute(lambda x: fake.last_name())
    credit_card = factory.LazyAttribute(
        lambda x: fake.credit_card_number() if random.choice([True, False]) else None
    )
    car_number = factory.LazyAttribute(lambda x: fake.bothify(text="?###??##"))


class ParkingFactory(factory.Factory):
    class Meta:
        model = Parking

    address = factory.LazyAttribute(lambda x: fake.address())
    opened = factory.LazyAttribute(lambda x: random.choice([True, False]))
    count_places = factory.LazyAttribute(lambda x: random.randint(1, 100))
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)
