import os

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from push_notifications.models import APNSDevice, GCMDevice

from .models import PushNotification
from .tasks import push_notification_send_all_user


def prepate_notification_data(instance):
    return {
        "id": str(instance.id),
        "address": instance.address,
        "city": instance.city,
        "state": instance.state,
        "zip_code": str(instance.zip_code),
        "email": instance.email,
        "phone_number": str(instance.phone_number),
        "owner_or_manager": instance.owner_or_manager,
        "picture": instance.picture.url if instance.picture else "",
        "website": str(instance.website),
        "industry": instance.industry,
        "description": instance.description,
        "total_zwes": str(instance.total_favourites),
    }


@receiver(post_save, sender=PushNotification)
def push_notification_send(sender, instance, created, **kwargs):
    # push_notification_send_all_user.delay(pk=instance.pk)

    notification_data = dict()
    notification_data["title"] = instance.title
    notification_data["body"] = instance.message if instance.message else ''
    notification_data["image"] = instance.image.url if instance.image else ''

    restaurant_data = {}
    if instance.restaurant:
        restaurant_data = prepate_notification_data(instance.restaurant)

    # GCMDevice.objects.all().send_message(
    #     message=notification_data, extra=restaurant_data)

    # APNSDevice.objects.all().send_message(
    #     message=notification_data, extra=restaurant_data)
    PushNotification.objects.update(
        title="", message="", image="", restaurant="")

    print(notification_data, restaurant_data)
