from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from .forms import SurveyForm, ClientForm, QuestionForm, MarkFormSet, QuestionFormSet, MarkForm
from .models import Survey, Client, Question, Mark


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

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'main/survey_detail.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем список вопросов в контекст
        context['questions'] = Question.objects.filter(survey=self.object)
        return context

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
    success_url = '/'

def survey_create_or_update(request, pk=None):
    # Если передан pk, получаем существующий Survey, иначе создаем новый
    survey = get_object_or_404(Survey, pk=pk) if pk else Survey()

    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        question_formset = QuestionFormSet(request.POST, instance=survey)

        if form.is_valid() and question_formset.is_valid():
            survey = form.save()
            questions = question_formset.save(commit=False)

            # Сохраняем вопросы и привязываем к survey
            for question in questions:
                question.survey = survey
                question.save()

            # Создаем mark_formsets после сохранения вопросов
            mark_formsets = [
                MarkFormSet(request.POST, instance=question, prefix=f'marks_{question.pk}')
                for question in survey.question_set.all()
            ]

            if all(mark_formset.is_valid() for mark_formset in mark_formsets):
                for mark_formset in mark_formsets:
                    mark_formset.save()

                return redirect(reverse('main:survey_detail_slug', kwargs={'slug': survey.slug}))
    else:
        form = SurveyForm(instance=survey)
        question_formset = QuestionFormSet(instance=survey)

        # Создаем mark_formsets только если у survey есть вопросы
        mark_formsets = [
            MarkFormSet(instance=question, prefix=f'marks_{question.pk}')
            for question in survey.question_set.all()
        ] if pk else []

    context = {
        'form': form,
        'question_formset': question_formset,
        'mark_formsets': mark_formsets,
        'survey': survey,
    }
    return render(request, 'main/survey_form.html', context)


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
    success_url = reverse_lazy('main:client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'main/client_confirm_delete.html'
    success_url = reverse_lazy('main:client_list')

class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'
    context_object_name = 'object_list'

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'main/create_question.html'

    def form_valid(self, form):
        # Привязываем вопрос к опросу
        form.instance.survey_id = self.kwargs['survey_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:survey_detail_slug',  kwargs={'slug': self.object.survey.slug})

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'main/update_question.html'

    def get_success_url(self):
        return reverse_lazy('main:survey_detail_slug', kwargs={'slug': self.object.survey.slug})

    def form_valid(self, form):
        formset = MarkFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'main/delete_question.html'

    def get_success_url(self):
        return reverse_lazy('main:survey_detail_slug', kwargs={'pk': self.object.survey.id})

class MarkListView(ListView):
    model = Mark
    template_name = 'main/mark_list.html'
    context_object_name = 'marks'

class MarkCreateView(CreateView):
    model = Mark
    form_class = MarkForm
    template_name = 'main/create_mark.html'
    success_url = reverse_lazy('main:mark_list')

class MarkUpdateView(UpdateView):
    model = Mark
    form_class = MarkForm
    template_name = 'main/update_mark.html'
    success_url = reverse_lazy('main:mark_list')

class MarkDeleteView(DeleteView):
    model = Mark
    template_name = 'main/delete_mark.html'
    success_url = reverse_lazy('main:mark_list')