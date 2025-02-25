from django.urls import reverse_lazy
from django.views import generic
from .models import User
from .forms import UserForm

class UserCreateView(generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(generic.UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

class UserDeleteView(generic.DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


class UserListView(generic.ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'object_list'  # Список пользователей будет доступен в шаблоне как object_list