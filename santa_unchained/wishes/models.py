from django.db import models
from django_extensions.db.fields import AutoSlugField

from santa_unchained.wishes.constants import WishListStatuses

# For longitude and latitude fields motivation:
# https://stackoverflow.com/questions/30706799/which-model-field-to-use-in-django-to-store-longitude-and-latitude-values


class Address(models.Model):
    """An address provided by a child where Santa should deliver presents."""

    street = models.CharField(
        max_length=100,
        verbose_name="Street",
        help_text="Street and number of a building.",
    )
    post_code = models.CharField(
        max_length=10, verbose_name="Postal code", help_text="Postal code."
    )
    city = models.CharField(max_length=100, verbose_name="City", help_text="City")
    country = models.CharField(
        max_length=100, verbose_name="Country", help_text="Country"
    )
    lng = models.DecimalField(
        verbose_name="Longitude",
        help_text="Address longitude.",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    lat = models.DecimalField(
        verbose_name="Latitude",
        help_text="Address latitude.",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"Child address: {', '.join([self.street, self.post_code, self.city, self.country])} ({self.pk=})"


class WishList(models.Model):
    """A wish list sent by a child to Santa."""

    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="Name of a child.",
    )
    email = models.EmailField(
        verbose_name="Email address",
        help_text="Email of a child.",
    )
    content = models.TextField(
        verbose_name="Letter to Santa",
        help_text="Child's letter to Santa.",
    )
    status = models.CharField(
        max_length=20,
        choices=WishListStatuses.choices,
        default=WishListStatuses.NEW,
        verbose_name="Status",
        help_text="Status of a wish list.",
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        help_text="An automatically generated slug (can be used to construct URLs).",
        populate_from="name",
    )
    address = models.ForeignKey(
        Address,
        verbose_name="A child's address",
        help_text="An address where the presents will be delivered.",
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
        verbose_name="A wish list",
        help_text="A relevant wish list the present belongs to.",
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="Name of a present.",
    )
    approved = models.BooleanField(
        verbose_name="Approved",
        help_text="Approved by Santa.",
        default=True,
    )

    def __str__(self):
        return f"Wish list item: {self.name} ({self.pk=})"
