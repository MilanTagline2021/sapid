from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin, messages
from django.db.models import Sum
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from users.models import User

from .models import (BannerImage, Menu, MenuItem, Restaurant,
                     RestaurantAddExcel, SaveMenuItem)

admin.site.register(RestaurantAddExcel, SingletonModelAdmin)


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 0
    max_num = 5


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    max_num = 200
    readonly_fields = ('total_favourites', 'total_saves')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture_get', 'address', 'city', 'state',
                    'zip_code', 'email', 'phone_number', 'owner_or_manager', 'website', 'industry', 'favourites', 'item_saves', 'item_favourites')
    readonly_fields = ('total_favourites',)
    search_fields = ('name', 'address', 'city', 'state', 'zip_code')

    def favourites(self, obj):
        return obj.total_favourites

    def item_saves(self, obj):
        menu_items = MenuItem.objects.filter(
            restaurant_id=obj.id).aggregate(Sum('total_saves'))
        return menu_items['total_saves__sum']

    def item_favourites(self, obj):
        menu_items = MenuItem.objects.filter(
            restaurant_id=obj.id).aggregate(Sum('total_favourites'))
        return menu_items['total_favourites__sum']

    def picture_get(self, obj):
        return format_html('<img src="{}" width="auto" height="50px" />'.format(obj.picture.url)) if obj.picture else '-'
    picture_get.short_description = "Picture"

    inlines = [
        BannerImageInline,
        MenuItemInline
    ]
