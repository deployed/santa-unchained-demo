from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from santa_unchained.wishes.constants import WishListStatuses
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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items").select_related("address")

    def items_count(self, obj):
        all_items = obj.items.count()
        approved_items = obj.items.filter(approved=True).count()
        return f"{approved_items}/{all_items}"

    items_count.short_description = _("approved/all items")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WishListNew)
class WishListNewAdmin(WishListBaseAdmin):
    actions = ['move_to_accept', 'move_to_reject']

    @admin.action(description=_("Accept"))
    def move_to_accept(self, request, queryset):
        updated = queryset.update(status=WishListStatuses.ACCEPTED)
        self.message_user(request, _("{} wish list(s) accepted.").format(updated), messages.SUCCESS)

    @admin.action(description=_("Reject"))
    def move_to_reject(self, request, queryset):
        updated = queryset.update(status=WishListStatuses.REJECTED)
        self.message_user(request, _("{} wish list(s) rejected.").format(updated), messages.SUCCESS)


@admin.register(WishListAccepted)
class WishListAcceptedAdmin(WishListBaseAdmin):
    actions = ['move_to_ready_for_shipping']

    @admin.action(description=_("Mark as ready for shipping"))
    def move_to_ready_for_shipping(self, request, queryset):
        updated = queryset.update(status=WishListStatuses.READY_FOR_SHIPPING)
        self.message_user(request, _("{} wish list(s) mark as ready for shipping.").format(updated), messages.SUCCESS)


@admin.register(WishListRejected)
class WishListRejectedAdmin(WishListBaseAdmin):
    pass


@admin.register(WishListReadyForShipping)
class WishListReadyForShippingAdmin(WishListBaseAdmin):
    actions = ['move_to_delivered']

    @admin.action(description=_("Mark as delivered"))
    def move_to_delivered(self, request, queryset):
        updated = queryset.update(status=WishListStatuses.DELIVERED)
        self.message_user(request, _("{} wish list(s) delivered.").format(updated), messages.SUCCESS)


@admin.register(WishListDelivered)
class WishListDeliveredAdmin(WishListBaseAdmin):
    pass
