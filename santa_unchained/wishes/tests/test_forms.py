import pytest
from django.forms import model_to_dict

from santa_unchained.wishes.factories import WishListFactory, AddressFactory, fake
from santa_unchained.wishes.forms import WishListWithAddressForm


@pytest.mark.django_db()
class TestWishListWithAddressForm:

    def test_valid(self):
        wish_list = WishListFactory()
        address = AddressFactory()
        data = model_to_dict(wish_list) | model_to_dict(address)
        data["items"] = "\n".join(fake.name() for _ in range(3))
        assert WishListWithAddressForm(data=data).is_valid()
