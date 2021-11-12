from django.urls import path

from . import views

urlpatterns = [
    path('update-db', views.update_db, name='update-db'),
    path('search', views.search, name='search'),
]
