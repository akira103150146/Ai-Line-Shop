"""
URL configuration for ai_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_posting_helper_page, name='get-posting-helper-page'),
    path("lut2/", include("lut2.urls", namespace="lut2")),
    path('admin/', admin.site.urls),
    path('line/', include('line_bot.urls')),
    path('api/users/<str:username>/', views.get_user_by_username, name='get-user-by-username'),
    # path('api/debug/',views.debug_environment, name='debug-environment')
]
