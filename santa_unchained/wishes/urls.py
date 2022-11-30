from django.urls import path

from santa_unchained.wishes.views import WishListFormView, WishListSuccessView

app_name = "wishes"

urlpatterns = [
    path("", WishListFormView.as_view(), name="wishlist"),
    path("success/<slug:slug>/", WishListSuccessView.as_view(), name="success")
]

