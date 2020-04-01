from django import forms
from treebay.models import Plant
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# Form for registering users
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'picture')


# Form for editing user profiles
class EditProfileForm(UserChangeForm):
    # Hides password from template
    password = None
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'picture')


# Form for adding a new plant
class PlantForm(forms.ModelForm):

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        super(PlantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Plant
        fields = ('name', 'description', 'price', 'location', 'categories', 'picture')
        exclude = ('stars', 'owner', 'isSold', 'views', 'uploadDate', 'slug')
