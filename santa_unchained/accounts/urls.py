from django.urls import path

from santa_unchained.accounts.views import IndexView

app_name = "accounts"

urlpatterns = [path("", IndexView.as_view(), name="index")]
