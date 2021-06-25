from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from budget_api import models
from django.contrib.auth import get_user_model


User = get_user_model()

class IncomeAndExpenseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncomeAndExpenseCategory
        fields = "__all__"

class UserBudgetListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]

class BudgetListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    shared_with = UserBudgetListSerializer(many=True)
    
    class Meta:
        model = models.Budget
        fields = ["id", "name", "owner", "balance", "shared_with"]

class IncomeAndExpenseSerializer(serializers.ModelSerializer):
    category = StringRelatedField()

    class Meta:
        model = models.Income
        fields = "__all__"

class IncomeAndExpenseCreationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Income
        fields = "__all__"

class BudgetDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    incomes  = IncomeAndExpenseSerializer(many=True)
    expenses = IncomeAndExpenseSerializer(many=True)

    class Meta:
        model = models.Budget
        fields = "__all__"

class BudgetSerializer(serializers.ModelSerializer):
    shared_with = UserBudgetListSerializer(many=True)

    class Meta:
        model = models.Budget
        fields = ["name", "incomes", "expenses", "shared_with"]

class IncomeSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.IncomeAndExpenseCategory.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.Income
        fields = "__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.IncomeAndExpenseCategory.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = models.Expense
        fields = "__all__"

class CreateBudgetSerializer(serializers.ModelSerializer):

    incomes = IncomeSerializer(many=True)
    expenses = ExpenseSerializer(many=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    shared_with = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = models.Budget
        fields = '__all__'

    def create(self, validated_data):
        incomes_validated_data = validated_data.pop('incomes')
        expenses_validated_data = validated_data.pop('expenses')
        budget = models.Budget.objects.create(**validated_data)
        incomes_serializer = self.fields['incomes']
        expenses_serializer = self.fields['expenses']

        incomes = incomes_serializer.create(incomes_validated_data)
        expenses = expenses_serializer.create(expenses_validated_data)        
        
        for expense in expenses:
            budget.expenses.add(expense)

        for income in incomes:
            budget.incomes.add(income)

        return budget
