import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from santa_unchained.wishes.constants import WishListStatuses
from santa_unchained.wishes.managers import (
    AcceptedWishListManager,
    DeliveredWishListManager,
    NewWishListManager,
    ReadyForShippingWishListManager,
    RejectedWishListManager,
)

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
        return f"{', '.join([self.street, self.post_code, self.city, self.country])}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not (self.lat and self.lng):
            self.lat, self.lng = self.find_lat_lng()
        super().save(force_insert, force_update, using, update_fields)

    def find_lat_lng(self):
        """
        Find location in OpenStreetMap and return coordinates.
        If API fail or not return any results, we return default coordinates 0, 0
        """
        default_lat_lng = (0, 0)
        try:
            url = (
                f"https://nominatim.openstreetmap.org/search.php?q={self}&format=jsonv2"
            )
            data = requests.get(url).json()
        except requests.exceptions.RequestException:
            return default_lat_lng
        if not data:
            return default_lat_lng
        lat = data[0].get("lat", 0)
        lng = data[0].get("lon", 0)
        return (lat, lng)


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

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return _("Wish list for {}").format(self.name)

    @classmethod
    def number_of_objects(cls):
        return cls.objects.count()


class WishListNew(WishList):
    objects = NewWishListManager()

    class Meta:
        proxy = True
        verbose_name = _("new wish list")
        verbose_name_plural = _("1. New wish lists")


class WishListAccepted(WishList):
    objects = AcceptedWishListManager()

    class Meta:
        proxy = True
        verbose_name = _("accepted wish list")
        verbose_name_plural = _("2. Accepted wish lists")


class WishListRejected(WishList):
    objects = RejectedWishListManager()

    class Meta:
        proxy = True
        verbose_name = _("rejected wish list")
        verbose_name_plural = _("3. Rejected wish lists")


class WishListReadyForShipping(WishList):
    objects = ReadyForShippingWishListManager()

    class Meta:
        proxy = True
        verbose_name = _("wish list ready for shipping")
        verbose_name_plural = _("4. Wish lists ready for shipping")


class WishListDelivered(WishList):
    objects = DeliveredWishListManager()

    class Meta:
        proxy = True
        verbose_name = _("delivered wish list")
        verbose_name_plural = _("5. Delivered wish lists")


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
        return _("Wish list item: {}").format(self.name)
