from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'tg_chat_id']
        labels = {
            'email': 'Почта',
            'tg_chat_id': 'Telegram Chat ID',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tg_chat_id': forms.TextInput(attrs={'class': 'form-control'}),
        }