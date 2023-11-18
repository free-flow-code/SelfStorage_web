from django.contrib import admin

from renta_warehouse.forms import OrderAdminForm
from renta_warehouse.models import WareHouse, Box, Order, BoxImage


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm

    def save_model(self, request, obj, form, change):
        if obj.actual_end_rent_date:
            obj.box.free = False
            obj.box.save()
        else:
            obj.box.free = True
            obj.box.save()
        super().save_model(request, obj, form, change)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    fields = ('number', 'warehouse', 'floor', 'length', 'width', 'height', 'square', 'price', 'free')
    readonly_fields = ('square',)


@admin.register(WareHouse)
class WareHouseAdmin(admin.ModelAdmin):
    fields = ('address', 'temperature', 'height', 'free_boxes', 'total_boxes', 'image', 'advantage')
    readonly_fields = ('free_boxes', 'total_boxes')


@admin.register(BoxImage)
class BoxImageAdmin(admin.ModelAdmin):
    list_display = ['number']
    raw_id_fields = ['box']
