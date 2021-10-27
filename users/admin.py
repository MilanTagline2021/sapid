from django.contrib import admin
from django.contrib.auth.models import Group
from django_celery_beat.models import (ClockedSchedule, CrontabSchedule,
                                       IntervalSchedule, PeriodicTask,
                                       SolarSchedule)
from push_notifications.models import WebPushDevice, WNSDevice
from solo.admin import SingletonModelAdmin

from .models import Feedback, PushNotification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_email', 'full_name',
                    'provider_type', 'device_type', 'is_superuser', ]
    fields = ['full_name', 'email', 'password', 'is_superuser']
    exclude = ('first_name', 'last_name',
               'groups', 'created_at', 'is_staff', 'user_permissions', 'date_joined', 'last_login', 'is_active')
    list_filter = ('provider_type', 'device_type',)
    search_fields = ('email', 'full_name')

    def get_email(self, obj):
        return obj.email if obj.email else "Guest user"
    get_email.short_description = "Email"

    def save_model(self, request, obj, form, change):
        # Override this to set the password to the value in the field if it's
        obj.is_staff = True
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'description')
    list_filter = ('feedback_type',)
    search_fields = ('user__email', 'user__full_name')


admin.site.register(PushNotification, SingletonModelAdmin)


admin.site.site_header = "Sapid App Admin"
admin.site.site_title = "Sapid App Admin"
admin.site.index_title = "Sapid App Admin"


admin.site.unregister(WNSDevice)
admin.site.unregister(WebPushDevice)
admin.site.unregister(Group)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
