from django.contrib import admin
from budget_api import models

# Register your models here.
admin.site.register(models.Budget)
admin.site.register(models.Expense)
admin.site.register(models.Income)
admin.site.register(models.SharedBudget)
admin.site.register(models.AccessType)
admin.site.register(models.IncomeAndExpenseCategory)