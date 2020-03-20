from django.contrib import admin
from treebay.models import Category, Plant
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')


# Replace the default UserAdmin with the custom one
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


class PlantInline(admin.TabularInline):
    model = Plant.categories.through


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'description')

    # This line displays the plants associated with each category
    inlines = [
        PlantInline,
    ]


# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Plant)
