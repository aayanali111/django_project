from django.urls import path
from . import views


urlpatterns = [
    path('api/users', views.get_users, name="get_users"),
    path('api/register', views.register_user, name="register_user"),
    path('api/update', views.update_user, name="update_user"),
    path('api/delete', views.delete_user, name="delete_user"),
]