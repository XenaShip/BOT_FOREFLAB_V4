from django.urls import path

from .apps import MainConfig
from .views import SurveyDetailView, SurveyCreateView, SurveyUpdateView, SurveyDeleteView, index, ClientListView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView, \
    MarkListView, MarkUpdateView, MarkCreateView, MarkDeleteView
from .views import survey_create_or_update
app_name = MainConfig.name

urlpatterns = [
    path('', index.as_view(), name='index'),

    # Опросы
    path('survey/create/', survey_create_or_update, name='survey_create'),
    path('survey/<int:pk>/edit/', survey_create_or_update, name='survey_form'),
    path('surveys/<int:pk>/delete/', SurveyDeleteView.as_view(), name='survey_confirm_delete'),
    path('surveys/<slug:slug>/', SurveyDetailView.as_view(), name='survey_detail_slug'),
    path('marks/', MarkListView.as_view(), name='mark_list'),
    path('marks/create/', MarkCreateView.as_view(), name='create_mark'),
    path('marks/<int:pk>/edit/', MarkUpdateView.as_view(), name='update_mark'),
    path('marks/<int:pk>/delete/', MarkDeleteView.as_view(), name='delete_mark'),


    # Вопросы
    path('surveys/<int:survey_id>/questions/create/', QuestionCreateView.as_view(), name='create_question'),
    path('questions/<int:pk>/edit/', QuestionUpdateView.as_view(), name='update_question'),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name='delete_question'),

    # Клиенты
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_confirm_delete'),
]