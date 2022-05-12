**Mir-Media: Django with templates Task** <br />

**Steps to run:** <br />
1-Create virtual env and workon it<br />
2-Cd to root folder then Install all requirements using 'pip install -r requirements.txt'<br />
3-Add .env file next to manage.py file then use env.example to set environment variables <br />
5- run migrate command 'python manage.py migrate' <br />
6- Run tests using 'python manage.py test' to test the logic and behavior <br /> <br />

**Notes:** <br />
1- When you run the project django will create logs folder at the root
contains django.log file  to write logs of servers
to follow the logs you can use 'tail -f path_to_your_project/logs/django.log' <br />
2- I used from django_extensions AutoSlugField to (prepopulated slug from title). <br />
3- Set WORKING_SETTINGS to DEV if you are using local environment and add in settings/dev.py your settings <br />
4- Custom Admin Panel to check Results and data <br /> <br />
5- usually i use celery and redis or rabbitMq for tasks like send mail but pythonAnyWhere free host doesn't support running celery workers,
so I used thread instead of celery tasks

**BY Eng. Ali Askar**