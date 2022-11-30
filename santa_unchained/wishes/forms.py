from django import forms

from santa_unchained.wishes.models import WishList


class WishListWithAddressForm(forms.ModelForm):
    street = forms.CharField(
        max_length=100,
        label="Street",
        help_text="Street and number of a building.",
    )
    post_code = forms.CharField(
        max_length=10, label="Postal code", help_text="Postal code."
    )
    city = forms.CharField(max_length=100, label="City", help_text="City")
    country = forms.CharField(
        max_length=100, label="Country", help_text="Country"
    )
    items = forms.CharField(
        widget=forms.Textarea,
        label="A wish list",
        help_text="A relevant wish list the present belongs to.",
    )

    class Meta:
        model = WishList
        fields = [
            "name",
            "email",
            "content",
        ]
