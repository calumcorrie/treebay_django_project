from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from treebay.models import Category, Plant, UserProfile, User
from treebay.forms import PlantForm, UserForm, UserProfileForm


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
    context_dict = {'categories': category_list, 'plant_interest': plant_list_interest, 'plant_date': plant_list_date,
                    'plant_views': plant_list_views}

    # Render the response and send it back!
    return render(request, 'treebay/index.html', context=context_dict)


# View for the about page
def about(request):
    return render(request, 'treebay/about')


# View for a single plant
def show_plant(request, plant_slug):

    # Context dictionary to hold data we need to pass through to template
    context_dict = {}

    # Find the plant using the passed through plant slug, which is unique
    try:
        plant = Plant.objects.get(slug=plant_slug)
        # Add it to the dictionary
        context_dict['plant'] = plant
        # Get associated plant categories
        plant_cats = plant.categories.all()
        # Add them to the context dict
        context_dict['cats'] = plant_cats

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


# View for adding a plant
# User must be logged in
@login_required
def add_plant(request):
    form = PlantForm(request.user)
    if request.method == 'POST':
        form = PlantForm(request.user, request.POST)

        # Check if form is valid
        if form.is_valid():
            #
            plant = form.save(commit=False)
            # set owner to the current user uploading plant
            # TODO - Owner linking to current user not working yet
            user = User.objects.get(id=request.user.id)
            profile = UserProfile.objects.get(user=user)
            plant.owner = profile
            plant.save()
            # redirect to homepage for now, can also redirect to a success page or such like
            return redirect('')
        else:
            # print form error
            print(form.errors)
    else:
        form = PlantForm(request.user)

    return render(request, 'treebay/add_plant.html', {'form':form})


def register(request):

    # a boolean for telling the template whether registration was successful
    # set to false initially, code changes value to true when reg succeeds
    registered = False

    # if it is a HTTP Post we want to process data
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'treebay/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Your Treebay account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'treebay/login.html')
