from typing import Optional

import django.db
from django.db import transaction
from django.urls import reverse

from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm
from django.views.generic.edit import FormView

from santa_unchained.wishes.models import WishList, Address, WishListItem
from django.utils.translation import gettext_lazy as _


def process_wishlist_with_address_and_items(
    form: WishListWithAddressAndItemsForm
) -> WishList | WishListWithAddressAndItemsForm:
    """
    Process a wish list form.

    If there are no errors, a new WishList instance (and related objects) will be created.
    Otherwise, a form populated with errors will be returned.

    :param form: A form to process
    :return: instance of form.
    """
    cleaned_data = form.cleaned_data
    try:
        with transaction.atomic():
            return create_wishlist_address_and_items(cleaned_data, form)
    except django.db.Error:
        form.add_error(None, _("Cannot process the wish list. Please try again later."))
        return form


def create_wishlist_address_and_items(cleaned_data, form) -> WishList:
    """
    Create a wish list instance.

    Also, create related address and wish list items based on the payload of the form.

    :param form: A form to process
    :return: instance of form.
    """
    address_data = {
        "street": cleaned_data["street"],
        "post_code": cleaned_data["post_code"],
        "city": cleaned_data["city"],
        "country": cleaned_data["country"],
    }
    address = Address.objects.create(**address_data)
    wish_list = form.save(commit=False)
    wish_list.address = address
    wish_list.save()
    items = [
        WishListItem(
            name=name,
            wish_list=wish_list
        )
        for name in cleaned_data["items"]
    ]
    WishListItem.objects.bulk_create(items)
    return wish_list


class WishListFormView(FormView):
    object: Optional[WishList] = None
    template_name = 'wish_list_form.html'
    form_class = WishListWithAddressAndItemsForm

    def get_success_url(self):
        # TODO: replace with success page
        return reverse("accounts:index")

    def form_valid(self, form):
        instance_or_forms = process_wishlist_with_address_and_items(form)
        if not isinstance(instance_or_forms, WishListWithAddressAndItemsForm):
            self.object = instance_or_forms
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
