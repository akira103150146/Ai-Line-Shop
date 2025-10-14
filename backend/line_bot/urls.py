from django.urls import path
from . import views

urlpatterns = [
    path('webhook/<str:channel_id>/', views.line_webhook, name='line-webhook'),
]