from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from solo.models import SingletonModel

alphanumeric_validation = RegexValidator(
    r'^[0-9a-zA-Z& ]*$', 'Only alphanumeric characters are allowed.')
phone_number_validation = RegexValidator(
    r'^([0-9\(\)\/\+ \-]*)$', 'Please enter valid phone number.')
numeric_validator = RegexValidator(r'^[0-9]*$', 'Only Numbers are allowed.')


class Restaurant(models.Model):
    name = models.CharField(max_length=255, validators=[
                            alphanumeric_validation])
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=255, validators=[
                            alphanumeric_validation])
    state = models.CharField(max_length=255, validators=[
                             alphanumeric_validation])
    zip_code = models.CharField(max_length=20, validators=[
        numeric_validator])
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, validators=[
        phone_number_validation])
    owner_or_manager = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(
        upload_to='restaurant-picture', blank=True, null=True)
    website = models.CharField(max_length=2000, blank=True, null=True)
    industry = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    total_favourites = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        db_table = 'restaurant'
        ordering = ['total_favourites']
        unique_together = ('name', 'city', 'zip_code')


class RestaurantAddExcel(SingletonModel):
    restaurant_excel = models.FileField(
        upload_to='restaurant-excel', validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls', 'xlsm', 'csv'])])

    def __str__(self):
        return 'Restaurant Excel'

    class Meta:
        verbose_name = "Restaurant Add Excel"
        verbose_name_plural = "Restaurant Add Excels"
        db_table = 'restaurant_excel'


class BannerImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner-image',)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = "Banner Image"
        verbose_name_plural = "Banner Images"
        db_table = 'banner_image'


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        db_table = 'menus'

    def clean(self):
        if Menu.objects.filter(name__iexact=self.name).first():
            raise ValidationError("Menu with this Name already exists.")


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, validators=[
                            alphanumeric_validation])
    total_favourites = models.PositiveIntegerField(default=0)
    total_saves = models.PositiveIntegerField(default=0)
    menu_image = models.ImageField(
        upload_to='menu-image', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        db_table = 'menu_item'


class SaveMenuItem(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.menu_item.name

    class Meta:
        verbose_name = "Save Menu Item"
        verbose_name_plural = "Save Menu Items"
        db_table = 'save_menu_item'
