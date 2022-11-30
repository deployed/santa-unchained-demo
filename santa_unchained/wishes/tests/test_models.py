import pytest

from santa_unchained.wishes.factories import (
    AddressFactory,
    WishListFactory,
    WishListItemFactory,
)
from santa_unchained.wishes.models import Address, WishListItem


@pytest.mark.django_db()
class TestAddressModel:
    def test_address(self):
        address = AddressFactory()
        assert isinstance(address, Address)

    def test_wishlist(self):
        wish_list = WishListFactory()
        assert isinstance(wish_list.address, Address)
        assert wish_list in wish_list.address.wish_lists.all()

    def test_wishlist_item(self):
        item = WishListItemFactory()
        assert isinstance(item, WishListItem)
        assert item in item.wish_list.items.all()
