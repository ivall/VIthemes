import requests

from django.conf import settings


def get_form_errors(form):
    """
    Get only error message from errors in form
    """
    errors_as_list = []
    errors = form.errors.as_data()
    for i in errors:
        errors_as_list += errors[i][0]
    return errors_as_list


def verify_captcha(captcha_response):
    """
    Verify captcha
    """
    if not captcha_response:
        return False

    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                      params={'secret': settings.RECAPTCHA_PRIVATE_KEY, 'response': captcha_response}).json()

    return r['success']
