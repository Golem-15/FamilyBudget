from django.http.response import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views import View
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import CurrentUserDefault

import budget_api.models as models
import budget_api.serializers as serializers

class BudgetList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BudgetListSerializer
    
    def get_queryset(self):
        user = self.request.user
        return models.Budget.objects.filter(Q(owner=user) | Q(shared_with__in=[user]))

class BudgetDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        response_data = serializers.BudgetDetailSerializer(
            models.Budget.objects.get(id=pk)
        ).data
        response_data['balance'] = sum([float(x['value']) for x in response_data['incomes']]) - sum([float(x['value']) for x in response_data['expenses']])
        return JsonResponse(response_data)

class CreateBudget(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Budget.objects.all()
    serializer_class = serializers.BudgetSerializer

    def perform_create(self, serializer):
        balance = sum(float(x.value) for x in serializer.validated_data['incomes']) - sum(float(x.value) for x in serializer.validated_data['expenses'])
        serializer.save(owner=self.request.user, balance=balance)
    
class UpdateBudget(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BudgetSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Budget.objects.filter(owner=user)

class DeleteBudget(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return models.Budget.objects.filter(owner=user)

class CreateExpense(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Expense.objects.all()
    serializer_class = serializers.IncomeAndExpenseCreationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpdateExpense(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.IncomeAndExpenseCreationSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Expense.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CreateIncome(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Income.objects.all()
    serializer_class = serializers.IncomeAndExpenseCreationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpdateIncome(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Income.objects.all()
    serializer_class = serializers.IncomeAndExpenseCreationSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Income.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ListIncomes(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Income.objects.all()
    serializer_class = serializers.IncomeAndExpenseCreationSerializer


class RenderBudgetList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'budget_list.html')

class RenderUserList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_list.html')

class RenderCreateBudget(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_budget.html')
