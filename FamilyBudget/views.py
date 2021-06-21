from django.contrib.auth.decorators import login_required
from re import template
from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.defaults import page_not_found
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from FamilyBudget import serializers
from FamilyBudget.forms import UserForm
from django.template import RequestContext


def handler404(request, *args, **argv):
    response = render('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response

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
    # fields = ['username', 'password', 'first_name', 'last_name', 'email']
    form_class = UserForm

    def get_success_url(self):
        return reverse_lazy('render-user-list')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserUpadteView(UpdateView):
    model = User
    form_class = UserForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            raise Http404('No user found matching the query')
        return super(UserUpadteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('my-account')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDeleteView(DeleteView):
    model = User

    def get_success_url(self):
        return reverse_lazy('render-user-list')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

# to be replaced with redirects to user list view
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserCreated(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_created.html')

# to be replaced with redirects to user list view
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserUpdated(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_updated.html')

# to be replaced with redirects to user list view
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDeleted(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_deleted.html')

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDetails(View):
    def get(self, request, pk, *args, **kwargs):
        user_data = serializers.UserSerializer(User.objects.get(id=pk)).data
        return render(request, 'user_details.html', context={'user_data': user_data})

@method_decorator(login_required(login_url='login'), name='dispatch')
class MyAccount(View):
    def get(self, request, *args, **kwargs):
        user_data = serializers.UserSerializer(User.objects.get(id=self.request.user.id)).data
        user_update_url = reverse_lazy('user-update', kwargs={'pk': self.request.user.id})
        return render(request, 'user_details.html', context={'user_data': user_data, 'user_update_url': user_update_url})