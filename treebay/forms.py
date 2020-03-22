from django import forms
from treebay.models import Plant, Category, UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


# Form for adding a new plant
class PlantForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PlantForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Plant
        fields = ('name', 'description', 'price', 'location', 'categories', 'picture')
        exclude = ('stars', 'owner', 'isSold', 'views', 'uploadDate', 'slug')