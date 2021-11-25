from django.urls import path

from . import views

urlpatterns = [
    path('delete-db', views.clear_db, name='delete-db'),
    path('add-conference', views.add_conference_details, name='add-conference'),
    path('search', views.search, name='search'),
    path('add-paper', views.add_paper, name='add-paper'),
    path('login', views.log_in, name='login'),
    path('signup', views.sign_up, name='signup'),
    path('logout', views.log_out, name='logout'),
]
