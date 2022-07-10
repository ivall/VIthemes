from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .utils.oauth2 import DiscordOauth
from .models import User


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Wylogowano poprawnie.')
    return redirect('/')


def discord_login(request):
    return redirect(DiscordOauth.discord_login_url)


def discord_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect('/')

    access_token = DiscordOauth.get_access_token(code)
    user_json = DiscordOauth.get_user_json(access_token)

    username = user_json.get("username")
    discord_id = user_json.get("id")
    print(user_json)

    user, created = User.objects.update_or_create(
        discord_id=discord_id, defaults={"username": username},
    )

    login(request, user)

    DiscordOauth.join_to_server(access_token, discord_id)
    messages.add_message(request, messages.SUCCESS, 'Zalogowano poprawnie.')
    return redirect('/')
