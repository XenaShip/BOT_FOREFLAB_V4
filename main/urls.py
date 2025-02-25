from django.urls import path
from .views import SurveyDetailView, SurveyCreateView, SurveyUpdateView, SurveyDeleteView, index

app_name = 'users'

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('add/', SurveyCreateView.as_view(), name='survey_create'),
    path('<slug:slug>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('<slug:slug>/edit/', SurveyUpdateView.as_view(), name='survey_form'),
    path('<slug:slug>/delete/', SurveyDeleteView.as_view(), name='survey_confirm_delete'),
]