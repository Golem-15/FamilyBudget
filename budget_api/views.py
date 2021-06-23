from django.http.response import HttpResponse, JsonResponse, Http404
from django.views.generic.list import ListView
from django.views import View
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import CurrentUserDefault
import json
from uuid import uuid4

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
        budget = models.Budget.objects.filter(id=pk).filter(Q(owner=request.user) | Q(shared_with__in=[request.user]))
        if budget:
            response_data = serializers.BudgetDetailSerializer(
                models.Budget.objects.get(id=pk)
            ).data
            response_data['balance'] = sum([float(x['value']) for x in response_data['incomes']]) - sum([float(x['value']) for x in response_data['expenses']])
            return JsonResponse(response_data)
        else:
            return JsonResponse({})

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

class IncomeAndExpenseCategories(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.IncomeAndExpenseCategory.objects.all()
    serializer_class = serializers.IncomeAndExpenseCategorySerializer

class IncomeList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.IncomeAndExpenseSerializer

    def get_queryset(self):
        return models.Income.objects.filter(budget__id=self.kwargs.get('pk'))

class ExpenseList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.IncomeAndExpenseSerializer

    def get_queryset(self):
        return models.Expense.objects.filter(budget__id=self.kwargs.get('pk'))


class RenderBudgetList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'budget_list.html')

class RenderUserList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_list.html')

class RenderCreateBudget(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_budget.html')

class RenderBudgetDetails(View):
    def get(self, request, pk, *args, **kwargs):
        budget = models.Budget.objects.filter(id=pk).filter(Q(owner=request.user) | Q(shared_with__in=[request.user]))

        if budget:
            incomes = serializers.IncomeAndExpenseSerializer(models.Income.objects.filter(budget__id=self.kwargs.get('pk')), many=True).data
            expenses = serializers.IncomeAndExpenseSerializer(models.Expense.objects.filter(budget__id=self.kwargs.get('pk')), many=True).data
            incomes = [{key:value if key != 'value' else float(value) for key,value in income.items()} for income in incomes]
            expenses = [{key:value if key != 'value' else -float(value) for key,value in expense.items()} for expense in expenses]
            return render(request, 'budget_details.html', context={'incomes': json.dumps(incomes), 'expenses': json.dumps(expenses)})
        else:
            raise Http404()

class RenderBudgetEdit(View):
    def get(self, request, pk, *args, **kwargs):
        budget = models.Budget.objects.filter(id=pk).filter(Q(owner=request.user) | Q(shared_with__in=[request.user]))

        if budget:
            incomes = serializers.IncomeAndExpenseSerializer(models.Income.objects.filter(budget__id=self.kwargs.get('pk')), many=True).data
            expenses = serializers.IncomeAndExpenseSerializer(models.Expense.objects.filter(budget__id=self.kwargs.get('pk')), many=True).data
            incomes = [{key:value if key != 'value' else float(value) for key,value in income.items()} for income in incomes]
            expenses = [{key:value if key != 'value' else -float(value) for key,value in expense.items()} for expense in expenses]
            shared_with = serializers.BudgetSerializer(budget, many=True).data[0]['shared_with']
            return render(request, 'budget_edit.html', context={'incomes': json.dumps(incomes), 'expenses': json.dumps(expenses), 'balance': budget[0].balance, 'shared_with': json.dumps(shared_with), 'name': budget[0].name})
        else:
            raise Http404()


@transaction.atomic
def CreateBudget(request):
    data = json.loads(request.body)
    balance = sum([float(x['value']) for x in data['incomes']]) - sum([float(x['value']) for x in data['expenses']])
    new_budget = models.Budget.objects.create(name=data['name'], owner=request.user, balance=balance)
    for income in data['incomes']:
        new_income = models.Income.objects.create(id=str(uuid4()), title=income['title'], value=income['value'], category=models.IncomeAndExpenseCategory.objects.get(id=income['category']), owner=request.user)
        new_budget.incomes.add(new_income)
    for expense in data['expenses']:
        new_expense = models.Expense.objects.create(id=str(uuid4()), title=expense['title'], value=expense['value'], category=models.IncomeAndExpenseCategory.objects.get(id=expense['category']), owner=request.user)
        new_budget.expenses.add(new_expense)
    for user in data['sharedWith']:
        new_budget.shared_with.add(user)

    return HttpResponse('Budget created successfully', status=201)