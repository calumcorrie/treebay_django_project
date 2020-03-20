from django.shortcuts import render
from treebay.models import Category, Plant

# Create your views here.

# View for the homepage
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
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['plant_interest'] = plant_list_interest
    context_dict['plant_date'] = plant_list_date
    context_dict['plant_views'] = plant_list_views

    return render(request, 'treebay/index.html', context_dict)


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





