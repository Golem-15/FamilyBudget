from django.urls import path
from budget_api import views

urlpatterns = [
    path('budget/list/', views.BudgetList.as_view(), name='budget-list'),
    path('budget/details/<int:pk>/', views.BudgetDetails.as_view(), name='budget-details'),
    path('budget/create/', views.CreateBudget.as_view(), name='budget-create'),
    path('budget/update/<int:pk>/', views.UpdateBudget.as_view(), name='budget-update'),
    path('budget/delete/<int:pk>/', views.DeleteBudget.as_view(), name='delete-budget'),
    path('expense/create/', views.CreateExpense.as_view(), name='expense-create'),
    path('expense/update/<int:pk>', views.UpdateExpense.as_view(), name='expense-update'),
    path('income/create/', views.CreateIncome.as_view(), name='income-create'),
    path('income/update/<int:pk>', views.UpdateIncome.as_view(), name='income-update'),
]