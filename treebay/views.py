from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Count
from django.urls import reverse
from treebay.models import Category, Plant, UserProfile
from treebay.forms import PlantForm, RegisterForm
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe


# View for the homepage
def index(request):
    # Query database for all categories
    category_list = Category.objects.all()

    # Query database for top 6 most viewed Plants
    plant_list_views = Plant.objects.order_by('-views')[:6]

    # Query database for top 6 plants in terms of interest
    plant_list_interest = Plant.objects.annotate(star_num=Count('starred')).order_by('-star_num')[:6]

    # Query database for 6 most recently added plants
    plant_list_date = Plant.objects.order_by('-uploadDate')[:6]

    # Context dictionary we fill with our lists and pass to template
    context_dict = {'categories': category_list, 'plant_interest': plant_list_interest, 'plant_date': plant_list_date,
                    'plant_views': plant_list_views}

    # Render the response and send it back!
    return render(request, 'treebay/index.html', context=context_dict)


# View for the about page
def about(request):
    return render(request, 'treebay/about.html')


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get the number of visits to a page.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits


# View for a single plant ad
# Plant slug is not used in the function, but is needed for the url mapping
def show_plant(request, plant_slug, plant_id):
    # Context dictionary to hold data we need to pass through to template
    context_dict = {}

    # Find the plant using the unique plant id
    try:
        plant = Plant.objects.get(id=plant_id)
        # Add it to the dictionary
        context_dict['plant'] = plant
        # Get associated plant categories
        plant_cats = plant.categories.all()
        # Add them to the context dict
        context_dict['cats'] = plant_cats
        # Call to cookie handler that counts the visits
        visitor_cookie_handler(request)
        # Update view count of the ad
        plant.views = request.session['visits']
        # Set isStarred to False by default
        context_dict['isStarred'] = False
        # Get the current user browsing the plant
        current_user = request.user.profile
        # Get all users who starred the plant
        user_stars_list = UserProfile.objects.filter(starred=plant)
        # If current user is in those who starred the plant, set isStarred to True
        if current_user in user_stars_list:
            context_dict['isStarred'] = True

    except Plant.DoesNotExist:
        # If we get here plant does not exist
        # Template should display message
        context_dict['plant'] = None

    response = render(request, 'treebay/show_plant.html', context=context_dict)
    return response


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


# View for a users dashboard
# User must be logged in
@login_required
def dashboard(request):
    # Create a context dictionary
    context_dict = {}
    # Get current user profile
    current_user = request.user.profile
    # Add the users plants to the context dictionary
    context_dict['plants'] = Plant.objects.all().filter(owner=current_user)
    # add the users starred plants to dictionary
    context_dict['starred'] = current_user.starred.all()

    return render(request, 'treebay/dashboard.html', context=context_dict)


# View for adding a plant
# User must be logged in
@login_required
def add_plant(request):
    form = PlantForm(request.user.profile)
    if request.method == 'POST':
        form = PlantForm(request.user, request.POST)

        # Check if form is valid
        if form.is_valid():

            plant = form.save(commit=False)

            # set owner to the current user uploading plant
            # This now works
            plant.owner = request.user.profile

            if 'picture' in request.FILES:
                plant.picture = request.FILES['picture']

            plant.save()
            # Below line needed to save the m2m field category for the plant
            form.save_m2m()
            # redirect to homepage for now, can also redirect to a success page or such like
            return redirect('treebay:index')
        else:
            # print form error
            print(form.errors)
    else:
        form = PlantForm(request.user)

    return render(request, 'treebay/add_plant.html', {'form': form})


# View for starring a plant
def star_plant(request, plant_id):

    # Get the current User
    current_user = request.user.profile
    # Get the current plant
    plant = Plant.objects.get(id=plant_id)
    current_user.starred.add(plant)

    return redirect('treebay:dashboard')


def login_or_register(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'Log In':

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('treebay:index')
                else:
                    messages.add_message(request, messages.ERROR, 'Your TreeBay account is disabled. Create a new one?')
                    form = RegisterForm()
                    return render(request,
                                  'treebay/login.html',
                                  context={'form': form})

            else:
                messages.add_message(request, messages.ERROR, 'Login failed. Invalid details.')
                form = RegisterForm()
                return render(request,
                              'treebay/login.html',
                              context={'form': form})

        elif request.POST.get('submit') == 'Register':
            form = RegisterForm(request.POST)

            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.email = form.cleaned_data.get('email')
                if 'picture' in request.FILES:
                    user.profile.picture = request.FILES['picture']

                user.save()

                # login user after registration
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect(reverse('treebay:index'))

            # Invalid registration form
            else:
                # Get all errors from the form
                message_text = ''
                for subject, list_of_errors in form.errors.as_data().items():
                    for error in list_of_errors:
                        for message in error.messages:
                            message_text += mark_safe(message + "<br/>")
                messages.add_message(request, messages.ERROR, mark_safe('Registration failed. Errors:<br/>' + message_text))
                form = RegisterForm()
                return render(request,
                              'treebay/login.html',
                              context={'form': form})

    else:
        form = RegisterForm()
        return render(request,
                      'treebay/login.html',
                      context={'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('treebay:index'))
