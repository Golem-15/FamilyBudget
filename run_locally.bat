set SECRET_KEY=10932x,ciau[djbn9\82y3h109w8eyu-asu9dlk
python manage.py migrate
py manage.py loaddata budget_api/fixtures/superuser_fixture.json
py manage.py loaddata budget_api/fixtures/budget_api_fixture.json
py manage.py runserver --settings FamilyBudget.local_settings
pause