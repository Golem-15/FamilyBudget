from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from budget_api import models

class BudgetListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = models.Budget
        fields = ["id", "name", "owner"]

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
        fields = "__all__"