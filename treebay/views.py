from django.shortcuts import render
from treebay.models import Category, Plant


def index(request):
    most_recent_list = Plant.objects.order_by('-uploadDate')[:6]
    most_interest_list = Plant.objects.order_by('-stars')[:6]
    most_viewed_list = Plant.objects.order_by('-views')[:6]
    # Display the first 25 categories as tags in homepage
    categories_list = Category.objects.all()[:25]

    context_dict = {'most_recent': most_recent_list, 'most_interest': most_interest_list,
                    'most_viewed': most_viewed_list, 'categories': categories_list}

    # Render the response and send it back!
    return render(request, 'treebay/index.html', context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Tries to find a category name slug with the given name
        # .get() returns one model instance or raises an exception if there's no category.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated plants.
        # The filter() will return a list of plant objects or an empty list.
        plants = Plant.objects.filter(categories=category)
        # Adds our results list to the template context under name plants.
        context_dict['plants'] = plants
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['plants'] = None

    # Go render the response and return it to the client.
    return render(request, 'treebay/category.html', context=context_dict)
