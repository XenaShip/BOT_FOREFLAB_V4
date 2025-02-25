from django.urls import path

from .apps import MainConfig
from .views import SurveyDetailView, SurveyCreateView, SurveyUpdateView, SurveyDeleteView, index, ClientListView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('add/', SurveyCreateView.as_view(), name='survey_create'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('<slug:slug>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('<slug:slug>/edit/', SurveyUpdateView.as_view(), name='survey_form'),
    path('<slug:slug>/delete/', SurveyDeleteView.as_view(), name='survey_confirm_delete'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_confirm_delete'),
]