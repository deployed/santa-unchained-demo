from typing import Optional

from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView, ModelFormMixin

from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm
from santa_unchained.wishes.models import WishList


class WishListFormView(ModelFormMixin, FormView):
    object: Optional[WishList] = None
    template_name = "wishes/wish_list_form.html"
    form_class = WishListWithAddressAndItemsForm

    def get_success_url(self):
        return reverse("wishes:success", kwargs={"slug": self.object.slug})


class WishListSuccessView(TemplateView):

    template_name = "wishes/wish_list_success.html"


class WishListDetailView(DetailView):
    model = WishList
