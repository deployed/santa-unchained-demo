from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from santa_unchained.wishes.models import WishListNew, WishListItem, WishListAccepted, WishListRejected, \
    WishListReadyForShipping, WishListDelivered


class WishListItemInline(admin.TabularInline):
    model = WishListItem
    extra = 0
    fields = ("name", "approved")

    def has_delete_permission(self, request, obj=None):
        return False


class WishListBaseAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "address", "items_count")
    search_fields = ("name", "content", "email", "address__city")
    readonly_fields = ("name", "email", "content", "address")
    list_filter = ("address__country",)
    inlines = [WishListItemInline]
    actions = []  # TODO:

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items").select_related("address")

    def items_count(self, obj):
        all_items = obj.items.count()
        approved_items = obj.items.filter(approved=True).count()
        return f"{approved_items}/{all_items}"

    items_count.short_description = _("approved/all items")

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(WishListNew)
class WishListNewAdmin(WishListBaseAdmin):
    pass


@admin.register(WishListAccepted)
class WishListAcceptedAdmin(WishListBaseAdmin):
    pass


@admin.register(WishListRejected)
class WishListRejectedAdmin(WishListBaseAdmin):
    pass


@admin.register(WishListReadyForShipping)
class WishListReadyForShippingAdmin(WishListBaseAdmin):
    pass


@admin.register(WishListDelivered)
class WishListDeliveredAdmin(WishListBaseAdmin):
    pass
