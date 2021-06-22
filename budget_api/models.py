from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Expense(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey("IncomeAndExpenseCategory", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.value}"

class Income(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey("IncomeAndExpenseCategory", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} {self.value}"

class IncomeAndExpenseCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Income and expense categories"    

    def __str__(self):
        return self.name

class AccessType(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

class SharedBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey("Budget", on_delete=models.CASCADE)
    access_type = models.ForeignKey("AccessType", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.budget.name} / {self.user.username}"

class Budget(models.Model):
    name = models.CharField(max_length=255)
    incomes = models.ManyToManyField("Income", blank=True)
    expenses = models.ManyToManyField("Expense", blank=True)
    owner = models.ForeignKey(User, null=False, related_name='owner', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_with')
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"
