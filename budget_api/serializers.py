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

    class Meta:
        model = models.Budget
        fields = ["name", "incomes", "expenses", "shared_with"]