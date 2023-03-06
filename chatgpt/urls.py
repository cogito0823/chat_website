from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.chat, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]
