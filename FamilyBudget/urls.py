from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls.conf import include
from django.views.generic import RedirectView
import FamilyBudget.views as ProjectViews
import budget_api.views as BudgetApiViews

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='home/')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/successful/', ProjectViews.LogoutSuccessful, name='logout-successful'),
    path('home/', ProjectViews.Homepage.as_view(), name='homepage'),
    path('user/create/', ProjectViews.UserCreateView.as_view(success_url="/user_created_success/"), name='user-create'),
    path('user/delete/<int:pk>/', ProjectViews.UserDeleteView.as_view(success_url="/user_deleted_success/"), name="user-delete"),
    path('user_created/', ProjectViews.UserCreated.as_view(), name='user-created'),
    path('user_deleted/', ProjectViews.UserDeleted.as_view(), name='user-deleted'),
]
