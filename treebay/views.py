from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import AnonymousUser
from django.core import serializers
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from treebay.forms import PlantForm, RegisterForm, EditProfileForm
from treebay.models import Category, Plant, UserProfile

LISTIC_CHUNK = 5
ORDER_BY_FIELDS = ["viewed", "starred", "latest", "price_asc", "price_desc"]

DASHBOARD_CHUNK = 5

HOT_BOUNDARY = 4


# View for the homepage
def index(request):
    # Query database for all categories
    category_list = Category.objects.all()

    # Query database for top 6 most viewed Plants
    plant_list_views = Plant.objects.filter(isSold=False).order_by('-views')[:6]

    # Query database for top 6 plants in terms of interest
    plant_list_interest = Plant.objects.filter(isSold=False).annotate(star_num=Count('starred')).order_by('-star_num')[
                          :6]

    # Query database for 6 most recently added plants
    plant_list_date = Plant.objects.filter(isSold=False).order_by('-uploadDate')[:6]

    visitor_cookie_handler(request)

    # Context dictionary we fill with our lists and pass to template
    context_dict = {'categories': category_list, 'plant_interest': plant_list_interest, 'plant_date': plant_list_date,
                    'plant_views': plant_list_views, 'visits': request.session['visits']}

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


def visitor_cookie_handler(request, plant=None):
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
        if plant is not None:
            Plant.objects.filter(pk=plant.id).update(views=plant.views + 1)
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits


# Helper method to extract error messages from form
def get_error_messages(form):
    # Get all errors from the form
    message_text = ''
    for subject, list_of_errors in form.errors.as_data().items():
        for error in list_of_errors:
            for message in error.messages:
                message_text += mark_safe(message)
    return message_text


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
        # Call to cookie handler that counts the visits, and update the count of the ad
        visitor_cookie_handler(request, plant)

        # Set isStarred to False by default
        context_dict['isStarred'] = False
        # If user is logged in
        if not isinstance(request.user, AnonymousUser):
            # Get the current user profile browsing the plant
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
    context_dict = {}

    try:
        # Tries to find a category name slug with the given name
        # .get() returns one model instance or raises an exception if there's no category.
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['plants'] = None
    else:
        # Retrieve all of the associated plants.
        # The filter() will return a list of plant objects or an empty list.

        plants = Plant.objects.filter(categories=category).filter(isSold=False)
        context_dict = listic(request, plants)
        context_dict['category'] = category
        context_dict['hot'] = HOT_BOUNDARY

    # Render the response and return it to the client.
    return render(request, 'treebay/category.html', context=context_dict)


def listic(request, plants):
    context_dict = {}

    try:
        orderfield = request.GET.get('orderBy', None)
        if orderfield not in ORDER_BY_FIELDS or orderfield == None:
            raise ValueError

    except ValueError:
        orderfield = ORDER_BY_FIELDS[0]

    try:
        position = int(request.GET.get('from', 0))
    except ValueError:
        position = 0

    if orderfield == ORDER_BY_FIELDS[0]:
        plants = plants.order_by('-views')
    elif orderfield == ORDER_BY_FIELDS[1]:
        plants = plants.annotate(stars=Count('starred')).order_by('-stars')
    elif orderfield == ORDER_BY_FIELDS[2]:
        plants = plants.order_by('-uploadDate')
    elif orderfield == ORDER_BY_FIELDS[3]:
        plants = plants.order_by('price')
    else:
        plants = plants.order_by('-price')

    allcount = len(plants);

    if position == None:
        position = 0

    plants = plants.annotate(stars=Count('starred'))[position:position + LISTIC_CHUNK]

    context_dict['plants'] = plants

    context_dict['order_by'] = orderfield

    context_dict['totalcount'] = allcount
    context_dict['chunkbeg'] = position + 1
    context_dict['chunkend'] = min(position + LISTIC_CHUNK, allcount)

    context_dict['pageprev'] = position > 0
    context_dict['pagenext'] = position + LISTIC_CHUNK < allcount
    context_dict['pageppos'] = position - LISTIC_CHUNK
    context_dict['pagenpos'] = position + LISTIC_CHUNK

    return context_dict


# View for a users dashboard
# User must be logged in
@login_required
def dashboard(request):
    # Create a context dictionary
    context_dict = {}
    # Get current user profile
    current_user = request.user.profile

    # Add the users plants to the context dictionary
    plants = Plant.objects.all().filter(owner=current_user).annotate(stars=Count('starred'))

    # add the users starred plants to dictionary
    starred = current_user.starred.all().annotate(stars=Count('starred'))

    context_dict['starred'] = starred
    context_dict['plants'] = plants

    context_dict['dchunk'] = DASHBOARD_CHUNK
    context_dict['hot'] = HOT_BOUNDARY

    return render(request, 'treebay/dashboard.html', context=context_dict)


# View to show another user's profile
def show_user(request, user_username=None, user_id=None):
    if user_username is None:
        if request.user.is_authenticated:
            return dashboard(request)

        return redirect(reverse('treebay:login'))

    context_dict = {}
    try:
        seller = UserProfile.objects.get(user__username=user_username)
    except UserProfile.DoesNotExist:
        context_dict['seller'] = None
        context_dict['plants'] = None
    else:
        if seller.user.id == request.user.id:
            return dashboard(request)

        plants = Plant.objects.all().filter(owner=seller)
        context_dict = listic(request, plants)
        context_dict['seller'] = seller
        context_dict['hot'] = HOT_BOUNDARY

    return render(request, 'treebay/show_user.html', context=context_dict)


# View for adding a plant
@login_required
def add_edit_plant(request, plant_slug=None, plant_id=None):
    context_dict = {}
    if plant_id is not None:
        plant = Plant.objects.get(pk=plant_id)
        context_dict["editing"] = True
    else:
        plant = Plant()
        context_dict["editing"] = False
        

    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        # Check if form is valid
        if form.is_valid():
            plant = form.save(commit=False)
            # Set owner to the current user uploading plant
            plant.owner = request.user.profile
            if 'picture' in request.FILES:
                plant.picture = request.FILES['picture']
            plant.save()
            # Below line needed to save the m2m field category for the plant
            form.save_m2m()
            return redirect('treebay:dashboard')
        else:
            message_text = get_error_messages(form)
            messages.add_message(request, messages.ERROR, mark_safe('Errors: ' + message_text))

    else:
        form = PlantForm(instance=plant)

    context_dict['form'] = form
    context_dict['plant'] = plant
    context_dict['monitors'] = [ "Name", "Description", "Location", "Price" ]
    
    return render(request, 'treebay/add_edit_plant.html', context=context_dict)


@login_required
def star_plant(request):
    # AJAX star plant

    try:
        plant_id = int(request.GET.get('id', -1))

        # 1 as in add star, 0 as in remove star
        intent = int(request.GET.get('action', 1))

        plant = Plant.objects.get(id=plant_id)
        if plant_id == -1 or intent not in [0, 1]:
            raise ValueError
    except (Plant.DoesNotExist, ValueError):
        return HttpResponse(-1)

    current_user = request.user.profile

    if intent == 1:
        # As in, is now starred
        retval = 1
        current_user.starred.add(plant)
    else:
        # As in is now removed
        retval = 0
        current_user.starred.remove(plant)

    current_user.save()
    return HttpResponse(retval)


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
                message_text = get_error_messages(form)
                messages.add_message(request, messages.ERROR, mark_safe('Registration failed. Errors: ' + message_text))
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
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            # Get the newly uploaded picture
            if 'picture' in request.FILES:
                request.user.profile.picture = request.FILES['picture']

            form.save()

        # Invalid registration form
        else:
            # Get the errors from the form
            message_text = get_error_messages(form)
            messages.add_message(request, messages.ERROR, mark_safe('Editing profile failed. Errors: ' + message_text))

        return redirect(reverse('treebay:dashboard'))


    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'treebay/edit_profile.html', context={'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

        else:
            # Get the errors from the form
            message_text = get_error_messages(form)
            messages.add_message(request, messages.ERROR, mark_safe('Password change failed. Errors: ' + message_text))

        return redirect(reverse('treebay:dashboard'))

    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'treebay/change_password.html', context={'form': form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Profile successfully deleted.')
        return redirect(reverse('treebay:index'))
    else:
        return render(request, 'treebay/delete_profile.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('treebay:index'))
