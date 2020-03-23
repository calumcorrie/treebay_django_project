from django.urls import path, re_path
from treebay import views

app_name = "treebay"

urlpatterns = [
                  path('', views.index, name='index'),
                  path('about/', views.about, name='about'),
                  path('<slug:category_name_slug>/', views.show_category, name='show_category'),
                  path('ad/<slug:plant_slug>-<int:plant_id>/', views.show_plant, name='show_plant'),
                  path('add_plant/', views.add_plant, name='add_plant'),
                  path('register/', views.register, name='register'),
                  path('login/', views.user_login, name='login'),
              ]