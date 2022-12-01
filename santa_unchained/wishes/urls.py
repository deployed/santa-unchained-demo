from django.urls import path

from santa_unchained.wishes.views import (
    WishListDetailView,
    WishListFormView,
    WishListSuccessView,
)

app_name = "wishes"

urlpatterns = [
    path("", WishListFormView.as_view(), name="wishlist"),
    path("success/<slug:slug>/", WishListSuccessView.as_view(), name="success"),
    path("<slug:slug>/", WishListDetailView.as_view(), name="wishlist-detail"),
]
