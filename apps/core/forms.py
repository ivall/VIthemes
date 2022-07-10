from django import forms

from .models import Theme
from .utils.utils import verify_captcha


class CreateThemeForm(forms.ModelForm):

    def clean(self):
        if not verify_captcha(self.data['g-recaptcha-response']):
            raise forms.ValidationError("Uzupełnij poprawnie captche")

    class Meta:
        model = Theme
        fields = ['name', 'primary_color', 'description', 'image', 'supported_theme', 'css']

        widgets = {
            'supported_theme': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super(CreateThemeForm, self).__init__(*args, **kwargs)
        self.fields['primary_color'].required = False