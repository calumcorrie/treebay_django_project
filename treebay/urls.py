from django.urls import path
from treebay import views

app_name = "treebay"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('ad/<slug:plant_slug>-<int:plant_id>/', views.show_plant, name='show_plant'),
    path('add_plant/', views.add_edit_plant, name='add_plant'),
    path('edit_plant/<slug:plant_slug>-<int:plant_id>/', views.add_edit_plant, name='edit_plant'),
    path('login/', views.login_or_register, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/edit/', views.edit_profile, name='edit_profile'),
    path('user/change-password/', views.change_password, name='change_password'),
    path('user/delete-profile/', views.delete_profile, name='delete_profile'),
    path('user/', views.dashboard, name='dashboard'),
    path('star/<int:plant_id>/', views.star_plant, name='star'),
    path('user/<slug:user_username>/', views.show_user, name='show_user'),
]
