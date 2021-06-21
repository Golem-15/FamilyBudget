from django.contrib.auth.decorators import login_required
from re import template
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()


@method_decorator(login_required(login_url='login'), name='dispatch')
class Homepage(View):
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'homepage.html')
        else:
            return redirect('login')

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password']

    def get_success_url(self):
        return reverse_lazy('user-created', kwargs={'username': self.object.username})


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    
# to be replaced with redirects to user list view
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserCreated(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_created.html')

# to be replaced with redirects to user list view
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDeleted(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_deleted.html')