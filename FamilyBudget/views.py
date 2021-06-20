from re import template
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import get_user_model

User = get_user_model()

def LogoutSuccessful(request):
    logout(request)
    render(request, template_name='logout_successful.html')


class Homepage(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'homepage.html')


class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password']

    def get_success_url(self):
        return reverse_lazy('user-created', kwargs={'username': self.object.username})


class UserDeleteView(DeleteView):
    model = User
    
# to be replaced with redirects to user list view
class UserCreated(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_created.html')

# to be replaced with redirects to user list view
class UserDeleted(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_deleted.html')