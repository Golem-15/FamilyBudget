# Generated by Django 3.0.8 on 2021-06-22 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeAndExpenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Income and expense categories',
            },
        ),
        migrations.CreateModel(
            name='SharedBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_api.AccessType')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_api.Budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_api.IncomeAndExpenseCategory')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_api.IncomeAndExpenseCategory')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='budget',
            name='expenses',
            field=models.ManyToManyField(blank=True, to='budget_api.Expense'),
        ),
        migrations.AddField(
            model_name='budget',
            name='incomes',
            field=models.ManyToManyField(blank=True, to='budget_api.Income'),
        ),
        migrations.AddField(
            model_name='budget',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budget',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_with', to=settings.AUTH_USER_MODEL),
        ),
    ]