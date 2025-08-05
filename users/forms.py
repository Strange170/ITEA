from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['user_type'] == 'seller':
            user.user_type = 'pending'
        else:
            user.user_type = self.cleaned_data['user_type']

        if commit:
            user.save()
        return user
