from django.urls import path, re_path

from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantApi.as_view(),
         name="get_all_restaurants"),
    path('restaurants/<pk>', views.RestaurantDetailApi.as_view(),
         name="get_restaurant"),

    path('<str:model_name>/<int:pk>/favourite/',
         views.FavouriteAddRemoveApi.as_view(), name="favourite_add_remove"),
    path('restaurants/favourite/',
         views.FavouriteRestaurantApi.as_view(), name="favourite_restaurant_list"),
    path('menu-item/favourite/',
         views.FavouriteMenuItemApi.as_view(), name="favourite_menu_item_list"),

    path('menu-item/<int:pk>/save/',
         views.SaveAddRemoveApi.as_view(), name="save_add_remove"),
    path('menu-item/save/',
         views.SaveMenuItemApi.as_view(), name="save_menu_item_list"),
    path('total-data/',
         views.total_data, name="total_data"),

]
