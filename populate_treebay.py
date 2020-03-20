import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'treebay_django_project.settings')

import django

django.setup()
from treebay.models import Category, Plant
from django.contrib.auth.models import User


def populate():
    users = {
        'andrea': {'email': 'andrea@gmail.com', 'password': 'andrea1234'},
        'mark': {'email': 'mark@gmail.com', 'password': 'mark1234'},
        'david': {'email': 'david@gmail.com', 'password': 'david1234'},
        'catherine': {'email': 'catherine@gmail.com', 'password': 'catherine1234'},
        'alice': {'email': 'alice@gmail.com', 'password': 'alice1234'},
        'tom': {'email': 'tom@gmail.com', 'password': 'tom1234'},
    }

    categories = {'houseplants': {'description': 'Plants that enjoy house music'},
                  'allergy friendly': {
                      'description': 'These plants have very little pollen and will never trigger you'},
                  'outdoor': {'description': 'Plants that enjoy house music'},
                  'evergreen': {'description': 'Its green. Ever green.'},
                  'seasonal': {'description': 'Sadly dead by October'},
                  'seed plants': {'description': 'More like self colonising'},
                  'edible': {'description': 'For the japanese jelly cakes'},
                  'medical': {'description': 'For the brownies'},
                  'succulent': {'description': 'The family of that Aloe you killed for face moisturizer'},
                  'herbs': {'description': 'Herbal tea or mojito? Your call! '},
                  }

    plants = {'Spikey boi': {'description': 'This lovely cactus is lonely and needs a new home',
                             'location': 'Maryhill Road, Glasgow'}}

    # clear all users except for staff
    delete_users()

    # Add categories to DB
    for cat, cat_data in categories.items():
        add_cat(cat, cat_data['description'])

    # Add users to DB
    for user, user_data in users.items():
        add_user(user, user_data['email'], user_data['password'])


def add_user(username, email, password):
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password)
    user.save()
    return user


def add_cat(name, description):
    c = Category.objects.get_or_create(name=name, description=description)[0]
    c.save()
    return c


def delete_users():
    for user in User.objects.all():
        if not user.is_staff:
            user.delete()


# Start execution here
if __name__ == '__main__':
    print('Starting Treebay population script...')
    populate()
