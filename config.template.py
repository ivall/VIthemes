# django config
DJANGO_SECRET_KEY = 'secret'
DJANGO_ADMIN_URL = 'secret'

# domains config
LOCAL_DOMAIN = '127.0.0.1:8000'
PUBLIC_DOMAIN = 'production_domain'

# discord config
DISCORD_CLIENT_ID = 'id'
DISCORD_CLIENT_SECRET = 'secret'
DISCORD_BOT_TOKEN = 'secret'  # for auto add to discord server
GUILD_ID = 'id'  # id of guild to add user after login

# recaptcha config
RECAPTCHA_PUBLIC = 'key'
RECAPTCHA_PRIVATE = 'secret'

# official themes
OFFICIAL_THEMES = (
    ("light", "jasny"),
    ("dark", "ciemny"),
    ("all", "wszystkie")
)