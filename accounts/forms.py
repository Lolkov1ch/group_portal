from django import forms
from .models import ProfileModel

class UserForm(forms.Form):
    class Meta:
        model = ProfileModel
        fields = {
            'nickname', 
            'about',
            'role'
            'favourite_genres', 
            'favourite_game',
            'github_link',
            'profile_picture'}