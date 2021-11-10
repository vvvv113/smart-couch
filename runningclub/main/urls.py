from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('price', views.price, name='price'),
    path('game', views.game, name='game'),
    path('payment', views.payment, name='payment'),
    path('registration', views.registration, name='registration'),
    path('authorisation', views.auth, name='auth'),
    path('logout', views.leave_profile, name='leave_profile'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit'),
    path('profile/<str:username>/new_post', views.new_post, name='post'),
    path('all_profiles', views.all_profiles, name='all_profiles'),

]