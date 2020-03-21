from django.contrib import admin
from treebay.models import Category, Plant, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# Replace the default UserAdmin with the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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
