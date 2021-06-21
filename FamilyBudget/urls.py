from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls.conf import include
from django.views.generic import RedirectView
import FamilyBudget.views as ProjectViews

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='home/')),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logged_out.html', next_page=None), name='logout'),
    path('home/', ProjectViews.Homepage.as_view(), name='homepage'),
    path('user/create/', ProjectViews.UserCreateView.as_view(), name='user-create'),
    path('my_account/', ProjectViews.MyAccount.as_view(), name='my-account'),
    path('user/details/<int:pk>/', ProjectViews.UserDetails.as_view(), name='user-details'),
    path('user/delete/<int:pk>/', ProjectViews.UserDeleteView.as_view(), name="user-delete"),
    path('user/update/<int:pk>/', ProjectViews.UserUpadteView.as_view(), name="user-update"),
    path('user_created/', ProjectViews.UserCreated.as_view(), name='user-created'),
    path('user_updated/', ProjectViews.UserUpdated.as_view(), name='user-updated'),
    path('user_deleted/', ProjectViews.UserDeleted.as_view(), name='user-deleted'),
    path('get/user_list/', ProjectViews.UserList.as_view(), name='get-user-list'),
    path('api/', include('budget_api.rest_api_urls')),
    path('budget_app/', include('budget_api.urls')),
]
