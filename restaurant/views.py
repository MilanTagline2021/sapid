import json

from django.core.serializers import serialize
from django.db.models import Sum
from django.http import Http404, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .models import MenuItem, Restaurant, SaveMenuItem
from .serializers import (MenuItemSerlizers, RestaurantSerializer,
                          SaveMenuItemSerlizers)


class RestaurantApi(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', 'address', 'city', 'zip_code']


class RestaurantDetailApi(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response({'error': {"restaurant_id": ["Please provide valid restaurant id."]}}, status=400)


class FavouriteMenuItemApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuItemSerlizers

    def get_queryset(self):
        favourite_menu_items_ids = self.request.user.favourite_menu_items.all().values_list('id',
                                                                                            flat=True)

        return MenuItem.objects.filter(id__in=favourite_menu_items_ids)


class FavouriteRestaurantApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        favourite_restaurant_ids = self.request.user.favourite_restaurants.all().values_list('id',
                                                                                             flat=True)
        return Restaurant.objects.filter(id__in=favourite_restaurant_ids)


class FavouriteAddRemoveApi(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, model_name, pk, format=None):
        is_favourite = request.GET.get('is_favourite')
        user = self.request.user
        if model_name == 'restaurants':
            if not Restaurant.objects.filter(pk=pk).exists():
                return Response({'error': {"restaurant_id": ["Please provide valid restaurant id."]}}, status=400)

            user.favourite_restaurants.add(
                pk) if is_favourite == 'true' else user.favourite_restaurants.remove(pk)
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(restaurant)
            restaurant_id = pk
        elif model_name == 'menu-item':
            if not MenuItem.objects.filter(pk=pk).exists():
                return Response({'error': {"menu_item_id": ["Please provide valid menu item id."]}}, status=400)

            user.favourite_menu_items.add(
                pk) if is_favourite == 'true' else user.favourite_menu_items.remove(pk)
            menuitem = MenuItem.objects.get(pk=pk)
            serializer = MenuItemSerlizers(menuitem)
            restaurant_id = menuitem.restaurant.id
        return Response({'status': True, 'id': pk, 'is_favourite': is_favourite, 'restaurant_id': restaurant_id, 'favourite_item': serializer.data})


class SaveAddRemoveApi(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        is_save = request.GET.get('is_save')
        user = self.request.user
        if not MenuItem.objects.filter(pk=pk).exists():
            return Response({'error': {"menu_item_id": ["Please provide valid menu item id."]}}, status=400)

        get_user = User.objects.filter(id=user.id, provider_type='guest')

        if get_user.exists():
            return Response({'error': {"message": ["This user is guest user..!!"]}}, status=403)

        if is_save == 'true':
            SaveMenuItem.objects.get_or_create(
                user_id=user.id, menu_item_id=pk)
        else:
            SaveMenuItem.objects.filter(
                user_id=user.id, menu_item_id=pk).delete()
        menuitem = MenuItem.objects.get(pk=pk)
        serializer = MenuItemSerlizers(menuitem)
        restaurant_id = menuitem.restaurant.id
        return Response({'status': True, 'id': pk, 'is_save': is_save, 'restaurant_id': restaurant_id, 'save_item': serializer.data})


class SaveMenuItemApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaveMenuItemSerlizers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['created_at', ]
    ordering_fields = ['created_at', 'menu_item__name',
                       'menu_item__restaurant__name']

    def get_queryset(self):
        return SaveMenuItem.objects.filter(user=self.request.user)


def total_data(request):
    data = {
        'total_users': User.objects.all().count(),
        'total_saves': MenuItem.objects.all().aggregate(Sum('total_saves'))['total_saves__sum'],
        'total_favourites':  MenuItem.objects.all().aggregate(Sum('total_favourites'))['total_favourites__sum'],
    }

    return JsonResponse(data)
