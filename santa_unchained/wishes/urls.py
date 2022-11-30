from django.urls import path

from santa_unchained.wishes.views import WishListFormView

app_name = "wishes"

urlpatterns = [path("", WishListFormView.as_view(), name="wishlist")]

