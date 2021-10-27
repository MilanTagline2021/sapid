from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from restaurant.models import MenuItem, Restaurant


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})


class User(AbstractUser):
    DEVICE_TYPE = (
        ('android', 'Android'),
        ('ios', 'IOS'),
    )
    PROVIDER_TYPE = (
        ('google', 'Google'),
        ('guest', 'Guest'),
        ('facebook', 'Facebook'),
        ('apple', 'Apple'),
        ('sapid_app', 'Sapid App'),
    )
    username = None
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, null=True)
    provider_type = models.CharField(
        max_length=20, choices=PROVIDER_TYPE, default='sapid_app')
    provider_user_id = models.CharField(max_length=255, blank=True)
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE)
    favourite_restaurants = models.ManyToManyField(
        Restaurant, blank=True, related_name="favourite_restaurants", verbose_name="Favourite Restaurants")
    favourite_menu_items = models.ManyToManyField(
        MenuItem, blank=True, related_name="favourite_menu_items", verbose_name="Favourite Menu Items")
    save_menu_items = models.ManyToManyField(
        MenuItem, blank=True, related_name="save_menu_items", verbose_name="Save Menu Items")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or 'Guest User'

    class Meta:
        ordering = ["id", "email"]
        db_table = 'users'

    objects = UserManager()


class Feedback(models.Model):
    FEEDBACK_TYPE = (
        ('overall_service', 'Overall Service'),
        ('customer_support', 'Customer Support'),
        ('add_restaurant', 'Add Restaurant'),
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    feedback_type = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        db_table = 'feedback'

    def __str__(self):
        return self.feedback_type


class PushNotification(models.Model):
    title = models.CharField(
        max_length=255, help_text="Add notification title here.")
    message = models.TextField(
        null=True, blank=True, help_text="Add notification message here.")
    image = models.ImageField(
        upload_to='notification-image', null=True, blank=True, help_text="Image view on recived notification.")
    restaurant = models.ForeignKey(
        Restaurant, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Push Notification {self.title}"

    class Meta:
        verbose_name = "Send Push Notification"
        verbose_name_plural = "Send Push Notifications"
        db_table = 'push_notification'
