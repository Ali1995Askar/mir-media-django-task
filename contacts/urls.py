from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.ContactCreateView.as_view(), name='send-email'),
]
