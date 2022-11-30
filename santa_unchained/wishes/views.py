from typing import Optional

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm
from django.views.generic.edit import FormView

from santa_unchained.wishes.models import WishList


class WishListFormView(FormView):
    object: Optional[WishList] = None
    template_name = 'wish_list_form.html'
    form_class = WishListWithAddressAndItemsForm

    def get_success_url(self):
        return reverse("wishes:success", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class WishListSuccessView(TemplateView):

    template_name = "wish_list_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(WishList, slug=self.kwargs["slug"])
        context['wishlist_url'] = instance.get_absolute_url()
        return context
