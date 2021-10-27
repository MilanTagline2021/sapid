from celery import shared_task

from .models import PushNotification


@shared_task
def push_notification_send_all_user(pk):
    excel = PushNotification.objects.get(pk=pk)
    print(excel)
    return "Notification Send to all user."
