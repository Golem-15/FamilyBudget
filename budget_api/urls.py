from django.urls import path
from budget_api import views

urlpatterns = [
    path('budget_list/', views.RenderBudgetList.as_view(), name='render-budget-list'),
    path('create_budget/', views.RenderCreateBudget.as_view(), name='render-create-budget'),
    path('user_list/', views.RenderUserList.as_view(), name='render-user-list'),
    path('budget_details/<int:pk>', views.RenderBudgetDetails.as_view(), name='render-budget-details'),
]