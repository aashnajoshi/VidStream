from django.urls import path, include
from tinymce import urls as tinymce_urls
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tinymce/', include(tinymce_urls)),
]