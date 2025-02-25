from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .forms import SurveyForm, ClientForm
from .models import Survey, Client


class index(generic.ListView):
    model = Survey
    template_name = 'main/index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        active_filter = self.request.GET.get('active', '')

        if active_filter == 'true':
            queryset = queryset.filter(active=True)
        elif active_filter == 'false':
            queryset = queryset.filter(active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем, есть ли активные опросы
        context['has_active_surveys'] = Survey.objects.filter(active=True).exists()
        return context

class SurveyDetailView(generic.DetailView):
    model = Survey
    template_name = 'main/survey_detail.html'
    slug_field = 'slug'  # Указываем поле для поиска объекта
    slug_url_kwarg = 'slug'  # Указываем имя параметра в URL

class SurveyCreateView(generic.CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'main/survey_form.html'
    success_url = '/'  # Редирект на главную страницу после успешного создания

class SurveyUpdateView(generic.UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'main/survey_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class SurveyDeleteView(generic.DeleteView):
    model = Survey
    template_name = 'main/survey_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = '/'
    # Редирект на главную страницу после успешного удаления

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_create.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_update.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'main/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'
    context_object_name = 'object_list'