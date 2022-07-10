import requests
from django.conf import settings
from config import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_BOT_TOKEN, GUILD_ID, LOCAL_DOMAIN, PUBLIC_DOMAIN


class DiscordOauth(object):
    def __init__(self):
        redirect_uri = self.redirect_uri

    client_id = DISCORD_CLIENT_ID
    client_secret = DISCORD_CLIENT_SECRET

    scope = "identify guilds.join"
    if settings.DEBUG:
        redirect_uri = f"http://{LOCAL_DOMAIN}/users/discord/callback"
    else:
        redirect_uri = f"https://{PUBLIC_DOMAIN}/users/discord/callback"

    discord_login_url = "https://discordapp.com/api/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(
        client_id, redirect_uri, scope)
    discord_token_url = "https://discordapp.com/api/oauth2/token"
    discord_api_url = "https://discordapp.com/api"

    @staticmethod
    def get_access_token(code):
        # post req to discord api. here is token, this is authen request
        payload = {
            'client_id': DiscordOauth.client_id,
            'client_secret': DiscordOauth.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': DiscordOauth.redirect_uri,
            'scope': DiscordOauth.scope
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = requests.post(
            url=DiscordOauth.discord_token_url, data=payload, headers=headers)
        json = access_token.json()
        return json.get("access_token")

    @staticmethod
    def get_user_json(access_token):
        url = DiscordOauth.discord_api_url + "/users/@me"

        headers = {
            "Authorization": "Bearer {}".format(access_token)
        }
        user_object = requests.get(url=url, headers=headers)
        user_json = user_object.json()
        return user_json

    def join_to_server(access_token, user_id):
        url = DiscordOauth.discord_api_url + f'/guilds/{GUILD_ID}/members/{user_id}'

        headers = {
            "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
            "Content-Type": "application/json",
        }
        data = {
            "access_token": access_token
        }
        requests.put(url=url, headers=headers, json=data)
