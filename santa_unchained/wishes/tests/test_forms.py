import pytest
from django.forms import model_to_dict

from santa_unchained.wishes.factories import AddressFactory, WishListFactory, fake
from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm
from santa_unchained.wishes.models import WishList


@pytest.mark.django_db()
class TestWishListWithAddressAndItemsForm:
    def test_valid(self):
        wish_list = WishListFactory()
        address = AddressFactory()
        data = model_to_dict(wish_list) | model_to_dict(address)
        items_names = [fake.name() for _ in range(3)]
        data["items"] = "\n".join(items_names)
        form = WishListWithAddressAndItemsForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data["items"] == items_names

        instance = form.save()
        assert isinstance(instance, WishList)
        assert instance.address is not None
        assert len(instance.items.all()) == len(items_names)
