from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Link UserProfile to a User model instance
    # The User model has username, email, password, date_joined and is_active attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes
    # TODO - add default image for when the user decides to omit it
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    NAME_MAX_LENGTH = 40
    DESCRIPTION_MAX_LENGTH = 200

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Plant(models.Model):
    NAME_MAX_LENGTH = 40
    DESCRIPTION_MAX_LENGTH = 200
    LOCATION_MAX_LENGTH = 30

    # Django generates a unique integer id automatically
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    # TODO - add default image for when the user decides to omit it
    picture = models.ImageField(upload_to='plant_images', blank=True)
    uploadDate = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    location = models.CharField(max_length=LOCATION_MAX_LENGTH)
    views = models.IntegerField(default=0)
    isSold = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Makes more sense to have this as an attribute "starred" in UserProfile
    # But I can't reference the Plant model before defining it
    # And it must be defined after UserProfile because of the "owner" attribute
    stars = models.ManyToManyField(UserProfile, related_name='stars')
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Plant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
