from django.db import models

from santa_unchained.wishes.constants import WishListStatuses


class NewWishListManager(models.Manager):
    """
    Manager which filter only new wish lists.
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=WishListStatuses.NEW)


class AcceptedWishListManager(models.Manager):
    """
    Manager which filter only accepted wish lists.
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=WishListStatuses.ACCEPTED)


class RejectedWishListManager(models.Manager):
    """
    Manager which filter only rejected wish lists.
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=WishListStatuses.REJECTED)


class ReadyForShippingWishListManager(models.Manager):
    """
    Manager which filter only wish lists ready for shipping.
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=WishListStatuses.READY_FOR_SHIPPING)


class DeliveredWishListManager(models.Manager):
    """
    Manager which filter only delivered wish lists.
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=WishListStatuses.DELIVERED)
