from allauth.account.forms import LoginForm
from django import forms

class CustomLoginForm(LoginForm):
    remember = forms.BooleanField(required=False, label='Remember me')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember'] = forms.BooleanField(required=False, initial=False, label='Remember me')

