from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.translation import ugettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@virginia.edu" not in data:   # any check you need
            raise forms.ValidationError("Must be a virginia.edu address")
        return data

    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name' ,'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name' ,'email']


class ProfileUpdateForm(forms.ModelForm):
    company = forms.CharField( required = False)
    position = forms.CharField( required = False)
    class Meta:

        model = Profile
        labels = {
            'year': _('Graduation Year'),
        }
        help_texts = {
            'image': _('Square images work best!'),
            'phone': ('No dashes or spaces please.')
        }
        fields = ['image','year', 'major','company','position','phone']



class ProfileSearchForm(forms.ModelForm):
    company = forms.CharField( required = False)
    position = forms.CharField( required = False)
    class Meta:
        model = Profile
        labels = {
            'year': _('Graduation Year'),
        }
        help_texts = {
            'image': _('Square images work best!'),
            'phone': ('No dashes or spaces please.')
        }
        fields = ['image','year','major','company','position','phone']
