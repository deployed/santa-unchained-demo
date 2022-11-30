from faker import Faker

from santa_unchained.wishes.models import Address
import factory

fake = Faker()


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = factory.LazyAttribute(lambda n: fake.street_name())
    post_code = factory.LazyAttribute(lambda n: fake.postcode())
    city = factory.LazyAttribute(lambda n: fake.city())
    country = factory.LazyAttribute(lambda n: fake.country())
