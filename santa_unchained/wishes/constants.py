from django.db import models
from django.utils.translation import gettext_lazy as _


class WishListStatuses(models.TextChoices):
    NEW = "NEW", _("New")
    ACCEPTED = "ACCEPTED", _("Accepted")
    REJECTED = "REJECTED", _("Rejected")
    READY_FOR_SHIPPING = "READY_FOR_SHIPPING", _("Ready for shipping")
    DELIVERED = "DELIVERED", _("Delivered")

    @classmethod
    def for_elf(cls):
        return [cls.ACCEPTED, cls.READY_FOR_SHIPPING]
