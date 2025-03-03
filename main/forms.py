from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from .models import Survey, Client, Question, Mark


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
SurveyFormSet = modelformset_factory(Survey, form=SurveyForm, extra=1)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'acc_tg', 'email', 'phone', 'tg_id']
        labels = {
            'name': 'ФИО',
            'acc_tg': 'Telegram аккаунт',
            'email': 'Почта',
            'phone': 'Номер телефона',
            'tg_id': 'Telegram ID',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'acc_tg': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tg_id': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'name': 'Полное имя клиента.',
            'acc_tg': 'Имя пользователя в Telegram (например, @username).',
            'email': 'Электронная почта клиента.',
            'phone': 'Номер телефона в формате +7XXXXXXXXXX.',
            'tg_id': 'Уникальный идентификатор пользователя в Telegram.',
        }

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark_text']
        labels = {
            'mark_text': 'Текст кнопки',
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['numb', 'que_text', 'type_q', 'wait_answer', 'file', 'kind_file']
        labels = {
            'numb': 'Номер вопроса',
            'que_text': 'Текст вопроса',
            'type_q': 'Тип вопроса',
            'wait_answer': 'Ожидание ответа',
            'file': 'Файл',
            'kind_file': 'Тип файла',
        }
        widgets = {
            'numb': forms.NumberInput(attrs={'class': 'form-control'}),
            'que_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type_q': forms.Select(attrs={'class': 'form-control'}),
            'wait_answer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'kind_file': forms.Select(attrs={'class': 'form-control'}),
        }
MarkFormSet = inlineformset_factory(
    Question,  # Родительская модель
    Mark,      # Дочерняя модель
    form=MarkForm,  # Форма для дочерней модели
    extra=1,  # Количество дополнительных пустых форм
    can_delete=True,  # Разрешить удаление кнопок
)
QuestionFormSet = inlineformset_factory(
    Survey,  # Родительская модель
    Question,  # Дочерняя модель
    form=QuestionForm,  # Форма для дочерней модели
    extra=1,  # Количество дополнительных пустых форм
    can_delete=True,  # Разрешить удаление вопросов
)
class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark_text', 'que']