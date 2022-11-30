import pytest

from santa_unchained.wishes.factories import AddressFactory
from santa_unchained.wishes.models import Address


@pytest.mark.django_db()
class TestAddressModel:

    def test_address(self):
        address = AddressFactory()
        assert isinstance(address, Address)

