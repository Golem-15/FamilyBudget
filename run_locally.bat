@echo off
set SECRET_KEY=10932x,ciau[djbn9\82y3h109w8eyu-asu9dlk
python manage.py migrate
python manage.py loaddata budget_api/fixtures/users_fixture.json
python manage.py loaddata budget_api/fixtures/budget_api_fixture.json
python manage.py runserver --settings FamilyBudget.local_settings