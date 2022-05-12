from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls', namespace='articles')),
    path('contact-us/', include('contacts.urls', namespace='contacts')),
    path('', TemplateView.as_view(template_name='basics/index.html'), name='home'),

]

