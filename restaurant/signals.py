from django.db.models import F
from django.db.models.signals import (m2m_changed, post_delete, post_save,
                                      pre_delete)
from django.dispatch import receiver
from users.models import User

from restaurant.models import (MenuItem, Restaurant, RestaurantAddExcel,
                               SaveMenuItem)

from .tasks import restaurant_adeed_on_excel


def favourite_add_remove(sender, instance, reverse, model, **kwargs):
    _id, = kwargs['pk_set'] if kwargs['pk_set'] else (0,)

    if kwargs['action'] == 'post_add' and _id:
        model.objects.filter(id=_id).update(
            total_favourites=F('total_favourites')+1)

    if kwargs['action'] == 'pre_remove' and _id:
        if model._meta.model_name == "restaurant":
            if User.objects.filter(id=instance.id, favourite_restaurants=_id):
                model.objects.filter(id=_id).update(
                    total_favourites=F('total_favourites')-1)
        elif model._meta.model_name == "menuitem":
            if User.objects.filter(id=instance.id, favourite_menu_items=_id):
                model.objects.filter(id=_id).update(
                    total_favourites=F('total_favourites')-1)


m2m_changed.connect(favourite_add_remove,
                    sender=User.favourite_menu_items.through)

m2m_changed.connect(favourite_add_remove,
                    sender=User.favourite_restaurants.through)


@receiver(post_save, sender=SaveMenuItem)
def memu_item_total_save_add(sender, instance, created, **kwargs):
    MenuItem.objects.filter(id=instance.menu_item_id).update(
        total_saves=F('total_saves')+1)


@receiver(post_delete, sender=SaveMenuItem)
def memu_item_total_save_remove(sender, instance, **kwargs):
    MenuItem.objects.filter(id=instance.menu_item_id).update(
        total_saves=F('total_saves')-1)


@receiver(pre_delete, sender=User)
def remove_favourite_restaurant(sender, instance, **kwargs):
    remove_restro_like = instance.favourite_restaurants.all().values_list('id', flat=True)
    if remove_restro_like:
        Restaurant.objects.filter(id__in=remove_restro_like).update(
            total_favourites=F('total_favourites')-1)


@receiver(pre_delete, sender=User)
def remove_favourite_menuitem(sender, instance, **kwargs):
    remove_menu_like = instance.favourite_menu_items.all().values_list('id', flat=True)
    if remove_menu_like:
        MenuItem.objects.filter(id__in=remove_menu_like).update(
            total_favourites=F('total_favourites')-1)


@receiver(post_save, sender=RestaurantAddExcel)
def restaurant_added_on_excel(sender, instance, created, **kwargs):
    if instance.restaurant_excel:
        restaurant_adeed_on_excel(pk=instance.pk)
        # restaurant_adeed_on_excel.delay(pk=instance.pk)
