from django.urls import path
from . import views

urlpatterns = [
    path('webhook/<int:business_id>/', views.line_webhook, name='line-webhook'),
]