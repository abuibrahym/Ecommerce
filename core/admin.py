from django.contrib import admin
from .models import Item, OrderItem, Order, BillingAddress, FavoriteItem

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'ordered']
    search_fields = ['ordered']
    list_filter = ['ordered']

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(FavoriteItem)
