from operator import itemgetter

from faker import Faker

from santa_unchained.wishes.constants import WishListStatuses
from santa_unchained.wishes.models import Address, WishList, WishListItem
import factory.fuzzy

fake = Faker()


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = factory.LazyAttribute(lambda n: fake.street_name())
    post_code = factory.LazyAttribute(lambda n: fake.postcode())
    city = factory.LazyAttribute(lambda n: fake.city())
    country = factory.LazyAttribute(lambda n: fake.country())


class WishListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishList

    email = factory.Faker("email")
    content = factory.Faker("sentences")
    name = factory.Faker("name")
    status = factory.fuzzy.FuzzyChoice(choices=WishListStatuses.choices, getter=itemgetter(0))
    address = factory.SubFactory(AddressFactory)


class WishListItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishListItem

    name = factory.fuzzy.FuzzyText()
    wish_list = factory.SubFactory(WishListFactory)
    approved = factory.fuzzy.FuzzyChoice(choices=(True, False))
