from django.shortcuts import render
from treebay.models import Category, Plant


def index(request):
    # Query database for all categories
    category_list = Category.objects.all()

    # Query database for top 5 (can be extended if required) most viewed Plants
    plant_list_views = Plant.objects.order_by('-views')[:5]

    # Query database for top 5 plants in terms of interest
    plant_list_interest = Plant.objects.order_by('-stars')[:5]

    # Query database for 5 most recently added plants
    plant_list_date = Plant.objects.order_by('-uploadDate')[:5]

    # Context dictionary we fill with our lists and pass to template
    context_dict = {'categories': category_list, 'plant_interest': plant_list_interest, 'plant_date': plant_list_date,
                    'plant_views': plant_list_views}

    # Render the response and send it back!
    return render(request, 'treebay/index.html', context=context_dict)


# View for the about page
def about(request):
    return render(request, 'treebay/about')


# View for a single plant
def show_plant(request, plant_name):
    # Context dictionary to hold data we need to pass through to template
    context_dict = {}

    # Find the plant using the passed through plant name, which is unique
    try:
        plant = Plant.objects.get(name=plant_name)

        # Add it to the dictionary
        context_dict['plant'] = plant

    except Plant.DoesNotExist:
        # If we get here plant does not exist
        # Template should display message
        context_dict['plant'] = None

    # Render response to return to client
    return render(request, 'treebay/show_plant.html', context=context_dict)


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

    # Render the response and return it to the client.
    return render(request, 'treebay/category.html', context=context_dict)
