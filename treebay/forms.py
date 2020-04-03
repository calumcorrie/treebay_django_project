from django import forms
from treebay.models import Plant, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# custom username validation - alphanumerical values only, user for reverse lookup
custom_username = forms.CharField(required=True, widget=forms.TextInput(
    attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '^[0-9a-zA-Z]*$'}))


# Form for registering users
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField(required=False)
    # custom username validation - alphanumerical values only, user for reverse lookup
    username = custom_username

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'picture')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # this changes the username field help_text
        self.fields['username'].help_text = 'Required. 150 characters or less. Only letters and numbers are allowed.'


# Form for editing user profiles
class EditProfileForm(UserChangeForm):
    # Hides password from template
    password = None
    picture = forms.ImageField(required=False)
    # custom username validation - alphanumerical values only, user for reverse lookup
    username = custom_username

    class Meta:
        model = User
        fields = ('username', 'email', 'picture')


# Form for adding a new plant
class PlantForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    description = forms.CharField(widget=forms.Textarea)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Plant
        fields = ('name', 'price', 'location', 'isSold', 'categories', 'description', 'picture')
