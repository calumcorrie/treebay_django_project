import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'treebay_django_project.settings')

import django

django.setup()
from treebay.models import Category, Plant, UserProfile
from django.contrib.auth.models import User


def populate():
    plants_alice = [{'name': 'Spiky boi', 'description': 'This lovely cactus needs a new home, water once in a while, '
                                                         'you can\'t kill it anyway.',
                     'location': 'Maryhill Road, Glasgow',
                     'categories': ['houseplants', 'succulent', 'cactus', 'allergy friendly'],
                     'price': 5},
                    {'name': 'Pink orchid', 'description': 'Extremely needy, having other orchid is recommended',
                     'location': 'Maryhill Road, Glasgow',
                     'categories': ['houseplants', 'orchid'],
                     'price': 20}
                    ]

    plants_tom = [{'name': 'Peace lily', 'description': 'This tropical shade-loving plant helps cleanse the air in '
                                                        'your room',
                   'location': 'Great Western Road, Glasgow',
                   'categories': ['houseplants', 'allergy friendly'],
                   'price': 0},
                  {'name': 'White orchid', 'description': 'Extremely needy, having other orchid is recommended',
                   'location': 'Great Western Road, Glasgow',
                   'categories': ['houseplants', 'orchid'],
                   'price': 15},
                  {'name': 'Aloe Vera', 'description': 'My best friend since freshman year. Needs a new loving family.',
                   'location': 'Great Western Road, Glasgow',
                   'categories': ['houseplants', 'succulent', 'allergy friendly'],
                   'price': 15}
                  ]

    plants_catherine = [{'name': 'Mini pine tree', 'description': 'Brought this lovely tree from a trip to Portugal. '
                                                                  'You must plant it outside, needs shade and sour '
                                                                  'soil.',
                         'location': 'Vincent Street, Glasgow',
                         'categories': ['outdoor', 'evergreen'],
                         'price': 10},
                        ]

    plants_david = [{'name': 'Mint pot', 'description': 'Couple of leaves gone because of an occasional mojito, '
                                                        'otherwise in pretty good shape. Need replanting in a bigger '
                                                        'pot',
                     'location': 'Buchanan Street, Glasgow',
                     'categories': ['houseplants', 'herbs', 'medical'],
                     'price': 10},
                    {'name': 'Tulips', 'description': 'Make your garden blossom next year with some lovely tulips',
                     'location': 'Buchanan Street, Glasgow',
                     'categories': ['houseplants', 'outdoor', 'seasonal', 'seed plants'],
                     'price': 2}
                    ]

    plants_liza = [{'name': 'Ficus', 'description': 'Grows quite slowly. Avoid moving it around the house, unless you '
                                                    'want to upset it.',
                    'location': 'Byres Road, Glasgow',
                    'categories': ['houseplants'],
                    'price': 12},
                   {'name': 'Mini red rose pot', 'description': 'The little roses need a lot of sun.',
                    'location': 'Byres Road, Glasgow',
                    'categories': ['houseplants', 'allergy friendly'],
                    'price': 8},
                   {'name': 'Purple kalanchoe', 'description': 'It has been alive for 3 months without water now.',
                    'location': 'Byres Road, Glasgow',
                    'categories': ['houseplants', 'allergy friendly'],
                    'price': 8}
                   ]

    plants_ben = [{'name': 'Anthurium Flamingo Flower', 'description': 'The plant would prefer to be in bright light, '
                                                                       'moist air and well-drained yet moist soil.',
                   'location': 'Shuna Street, Glasgow',
                   'categories': ['houseplants', 'seasonal'],
                   'price': 7},
                  {'name': 'Mini palm', 'description': 'Stole it from a garden in Turkey. No idea how to take care of '
                                                       'it.',
                   'location': 'Shuna Street, Glasgow',
                   'categories': ['outdoor'],
                   'price': 6},
                  {'name': 'Borage/Starflower', 'description': 'Needs sun and little water. Blossoms can be used for '
                                                               'cake decoration.',
                   'location': 'Shuna Street, Glasgow',
                   'categories': ['houseplants', 'allergy friendly', 'edible'],
                   'price': 18},
                  ]

    users = {
        'andrea': {'email': 'andrea@gmail.com', 'password': 'andrea1234'},
        'mark': {'email': 'mark@gmail.com', 'password': 'mark1234'},
        'david': {'email': 'david@gmail.com', 'password': 'david1234', 'plants': plants_david},
        'catherine': {'email': 'catherine@gmail.com', 'password': 'catherine1234', 'plants': plants_catherine},
        'alice': {'email': 'alice@gmail.com', 'password': 'alice1234', 'plants': plants_alice},
        'tom': {'email': 'tom@gmail.com', 'password': 'tom1234', 'plants': plants_tom},
        'elizabeth': {'email': 'liza@gmail.com', 'password': 'liza1234', 'plants': plants_liza},
        'ben': {'email': 'ben@gmail.com', 'password': 'ben1234', 'plants': plants_ben},
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
                  'herbs': {'description': 'Herbal tea or mojito? Your call!'},
                  'cactus': {'description': 'Has been lonely in the desert for so long, kinda'},
                  'orchid': {'description': 'If you want to adopt one of these beautiful creatures, keep in mind that '
                                            'they want as much attention as a woman '},
                  }

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
