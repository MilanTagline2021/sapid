import json
import os

import pandas as pd
from celery import shared_task
from django.db import transaction

from .models import Menu, MenuItem, Restaurant, RestaurantAddExcel


# @shared_task
def restaurant_adeed_on_excel(pk):
    uploded_file = RestaurantAddExcel.objects.get(pk=pk)
    name, extension = os.path.splitext(uploded_file.restaurant_excel.name)

    if extension == '.csv':
        restaurants = pd.read_csv(uploded_file.restaurant_excel).fillna('')
    else:
        restaurants = pd.read_excel(uploded_file.restaurant_excel).fillna('')

    excel_header = set(restaurants.columns.tolist())
    if excel_header == {'Name', 'Address', 'City', 'State', 'Zip Code', 'Email', 'Phone Number', 'Owner / Manager', 'Website', 'Industry', 'Menu Items (comma separated)', 'Description'}:
        for index, restaurant in restaurants.iterrows():
            name = restaurant['Name']
            address = restaurant['Address']
            city = restaurant['City']
            state = restaurant['State']
            zip_code = int(restaurant['Zip Code'])
            email = restaurant['Email']
            phone_number = restaurant['Phone Number']
            owner_or_manager = restaurant['Owner / Manager']
            website = restaurant['Website']
            industry = restaurant['Industry']
            excl_menu_list = restaurant['Menu Items (comma separated)']
            description = restaurant['Description']

            if not Restaurant.objects.filter(name=name, city=city, zip_code=zip_code).exists():
                try:
                    try:
                        # Duplicates should be prevented.
                        with transaction.atomic():
                            restaurant = Restaurant.objects.create(
                                name=name, address=address, city=city, state=state, zip_code=zip_code, email=email, phone_number=phone_number,
                                owner_or_manager=owner_or_manager, website=website, industry=industry, description=description)
                            menu_list = json.loads(excl_menu_list)
                            save_menu_item(restaurant, menu_list)
                    except:
                        pass

                except:
                    pass

    RestaurantAddExcel.objects.filter(pk=pk).update(restaurant_excel='')
    return "All restaurant added in our database on uploded excel."


def save_menu_item(restaurant, menu_list):
    new_menu_item_list = []
    for item_name in menu_list:
        if not MenuItem.objects.filter(restaurant=restaurant, name=item_name.strip()).exists():
            create = MenuItem.objects.create(
                restaurant=restaurant, name=item_name.strip())
