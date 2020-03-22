import os
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'treebay_django_project.settings')

import django

django.setup()
from treebay.models import Category, Plant, UserProfile
from django.contrib.auth.models import User


def populate():

    # all plants
    plants = pd.read_excel("treebay_testing_data/plants.xlsx", index_col=0)
    # all users
    users = pd.read_excel("treebay_testing_data/users.xlsx", index_col=0).to_dict("index")

    # add plants to users
    for username in plants.index.unique():
        users[username]['plants'] = plants.loc[plants.index == username].to_dict(orient='records')

    # all categories
    categories = pd.read_excel("treebay_testing_data/categories.xlsx", index_col=0).to_dict("index")

    # clear all users except for staff
    delete_users()
    # clear categories and plants
    delete_categories()
    delete_plants()

    # Add categories to DB
    for cat, cat_data in categories.items():
        add_cat(cat, cat_data['description'])

    # Add users to DB
    for username, user_data in users.items():
        user = add_user(username, user_data['email'], user_data['password'])

        user_profile = add_user_profile(user)
        user_profile.save()

        if 'plants' in user_data.keys():
            for plant_data in user_data['plants']:
                add_plant(user_profile, plant_data['name'], plant_data['description'], plant_data['location'],
                          plant_data['categories'], plant_data['price'])


def add_user(username, email, password):
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password)
    user.save()
    return user


# TODO add picture
def add_user_profile(user):
    user_profile = UserProfile.objects.get_or_create(user_id=user.id)[0]
    user_profile.save()
    return user_profile


def add_cat(name, description):
    c = Category.objects.get_or_create(name=name, description=description)[0]
    c.save()
    return c


def add_plant(owner, name, description, location, categories, price=0.0):
    p = Plant.objects.get_or_create(owner=owner, name=name, description=description, price=price, location=location)[0]
    p.categories.add(*Category.objects.filter(name__in=categories))
    p.save()
    return p


def delete_users():
    for user_profile in UserProfile.objects.all():
        if not user_profile.user.is_staff:
            user_profile.delete()


def delete_categories():
    for cat in Category.objects.all():
        cat.delete()


def delete_plants():
    for plant in Plant.objects.all():
        plant.delete()


# Start execution here
if __name__ == '__main__':
    print('Starting Treebay population script...')
    populate()
