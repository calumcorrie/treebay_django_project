from django import forms
from treebay.models import Plant, Category
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
    price = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Plant
        fields = ('name', 'price', 'location', 'isSold', 'categories', 'description',  'picture')
