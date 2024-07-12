from django.urls import path
from .views import *


app_name = 'graf'

urlpatterns = [
    path('', my_profile, name='my_profile'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile_detail/<int:user_id>/', profile_detail, name='profile_detail'),
    path('create_weekly_schedule/<int:user_id>/', create_weekly_schedule, name='create_weekly_schedule'),
    path('edit_schedule/<int:pk>/', edit_schedule, name='edit_schedule'),
    path('delete_schedule/<int:pk>/', delete_schedule, name='delete_schedule'),
    path('all_addresses/', all_addresses_schedule, name='all_addresses_schedule'),
]