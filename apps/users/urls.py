from django.urls import path
from .views import discord_login, logout_user, discord_callback

urlpatterns = [
    path('logout', logout_user, name='logout user'),
    path('discord/login', discord_login, name='login user using discord'),
    path('discord/callback', discord_callback, name='get user data from discord oauth'),
]