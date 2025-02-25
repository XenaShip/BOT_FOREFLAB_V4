from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['slug', 'name', 'description', 'active', 'counting', 'hello_text']
        labels = {
            'slug': 'Slug',
            'name': 'Название опроса',
            'description': 'Описание опроса',
            'active': 'Активность опроса',
            'counting': 'Количество вопросов',
            'hello_text': 'Приветственный текст',
        }
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'counting': forms.NumberInput(attrs={'class': 'form-control'}),
            'hello_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'slug': 'Уникальный идентификатор опроса (только латинские буквы, цифры, дефисы и подчеркивания).',
            'name': 'Краткое название опроса.',
            'description': 'Подробное описание опроса.',
            'active': 'Отметьте, если опрос активен.',
            'counting': 'Количество вопросов в опросе (необязательно).',
            'hello_text': 'Текст, который будет показан пользователю перед началом опроса (необязательно).',
        }