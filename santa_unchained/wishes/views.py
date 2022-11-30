from typing import Optional

from django.urls import reverse

from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm
from django.views.generic.edit import FormView

from santa_unchained.wishes.models import WishList


class WishListFormView(FormView):
    object: Optional[WishList] = None
    template_name = 'wish_list_form.html'
    form_class = WishListWithAddressAndItemsForm

    def get_success_url(self):
        # TODO: replace with success page
        return reverse("accounts:index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
