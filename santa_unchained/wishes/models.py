from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from santa_unchained.wishes.constants import WishListStatuses

# For longitude and latitude fields motivation:
# https://stackoverflow.com/questions/30706799/which-model-field-to-use-in-django-to-store-longitude-and-latitude-values


class Address(models.Model):
    """An address provided by a child where Santa should deliver presents."""

    street = models.CharField(
        max_length=100,
        verbose_name=_("Street"),
        help_text=_("Street and number of a building."),
    )
    post_code = models.CharField(
        max_length=10, verbose_name=_("Postal code"), help_text=_("Postal code.")
    )
    city = models.CharField(max_length=100, verbose_name=_("City"), help_text=_("City"))
    country = models.CharField(
        max_length=100, verbose_name=_("Country"), help_text=_("Country")
    )
    lng = models.DecimalField(
        verbose_name=_("Longitude"),
        help_text=_("Address longitude."),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    lat = models.DecimalField(
        verbose_name=_("Latitude"),
        help_text=_("Address latitude."),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return (
            f"Child address: "
            f"{', '.join([self.street, self.post_code, self.city, self.country])}"
            f" ({self.pk=})"
        )


class WishList(models.Model):
    """A wish list sent by a child to Santa."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of a child."),
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        help_text=_("Email of a child."),
    )
    content = models.TextField(
        verbose_name=_("Letter to Santa"),
        help_text=_("Child's letter to Santa."),
    )
    status = models.CharField(
        max_length=20,
        choices=WishListStatuses.choices,
        default=WishListStatuses.NEW,
        verbose_name=_("Status"),
        help_text=_("Status of a wish list."),
    )
    slug = AutoSlugField(
        verbose_name=_("Slug"),
        help_text=_("An automatically generated slug (can be used to construct URLs)."),
        populate_from="name",
    )
    address = models.ForeignKey(
        Address,
        verbose_name=_("A child's address"),
        help_text=_("An address where the presents will be delivered."),
        on_delete=models.PROTECT,
        related_name="wish_lists",
        related_query_name="wish_list",
    )

    def __str__(self):
        return f"Wish list for {self.name} ({self.pk=})"


class WishListItem(models.Model):
    """An item (present) a child wished for in the wish list sent to Santa."""

    wish_list = models.ForeignKey(
        WishList,
        verbose_name=_("A wish list"),
        help_text=_("A relevant wish list the present belongs to."),
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of a present."),
    )
    approved = models.BooleanField(
        verbose_name=_("Approved"),
        help_text=_("Approved by Santa."),
        default=False,
    )

    def __str__(self):
        return f"Wish list item: {self.name} ({self.pk=})"
