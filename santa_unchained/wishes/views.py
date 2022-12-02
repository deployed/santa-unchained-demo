from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView

from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm
from santa_unchained.wishes.models import WishList


class WishListFormView(CreateView):
    model = WishList
    form_class = WishListWithAddressAndItemsForm

    def get_success_url(self):
        return reverse("wishes:success", kwargs={"slug": self.object.slug})


class WishListSuccessView(TemplateView):
    template_name = "wishes/wishlist_success.html"


class WishListDetailView(DetailView):
    model = WishList
