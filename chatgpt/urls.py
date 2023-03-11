from django.urls import path, include
from . import views

urlpatterns = [
    path('chat/', views.chat, name='index'),
    path('', views.chat),
    path('chat/accounts/', include('django.contrib.auth.urls')),
    path("chat/register", views.register_request, name="register"),
    path("chat/logout", views.logout_request, name="logout"),
]
