from pytest_factoryboy import register

from santa_unchained.wishes.factories import AddressFactory, WishListFactory, WishListItemFactory

register(AddressFactory)
register(WishListFactory)
register(WishListItemFactory)
