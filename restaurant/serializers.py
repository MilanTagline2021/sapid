from collections import defaultdict

from django.conf import settings
from rest_framework import serializers

from .models import BannerImage, MenuItem, Restaurant, SaveMenuItem


class BannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImage
        fields = ('image',)


class MenuItemSerlizers(serializers.ModelSerializer):
    menu_image = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField('get_restaurant')

    class Meta:
        model = MenuItem
        fields = ('restaurant',  'id',  'name', 'total_favourites',
                  'total_saves', 'menu_image',)

    def get_menu_image(self, obj):
        return obj.menu_image.url if obj.menu_image else ''

    def get_restaurant(self, obj):
        restaurant_details = {'id': obj.restaurant.id,
                              'name': obj.restaurant.name,
                              'address': obj.restaurant.address,
                              'city': obj.restaurant.city,
                              'state': obj.restaurant.state,
                              'zip_code': obj.restaurant.zip_code,
                              'phone_number': obj.restaurant.phone_number,
                              }

        return restaurant_details


class RestaurantSerializer(serializers.ModelSerializer):
    banner_images = serializers.StringRelatedField(
        source='bannerimage_set', many=True)
    menus = serializers.SerializerMethodField('get_menu_items')

    def get_menu_items(self, instance):
        menu_items_all = instance.menuitem_set.all()
        menuItems = []
        for item in menu_items_all:
            menuItems.append(MenuItemSerlizers(item).data)
        return menuItems

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'city', 'state', 'zip_code', 'email',
                  'phone_number', 'owner_or_manager', 'picture', 'website', 'industry', 'banner_images', 'menus', 'total_favourites',)


class SaveMenuItemSerlizers(serializers.ModelSerializer):
    menu_item = MenuItemSerlizers()

    class Meta:
        model = SaveMenuItem
        fields = ('user_id', 'created_at', 'menu_item')
