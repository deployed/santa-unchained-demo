from django.db import models


class WishListStatuses(models.TextChoices):
    NEW = "NEW", "New"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    READY_FOR_SHIPPING = "READY_FOR_SHIPPING", "Ready for shipping"
    DELIVERED = "DELIVERED", "Delivered"
