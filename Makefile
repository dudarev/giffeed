MANAGE= python manage.py
HMANAGE= heroku run python manage.py

run:
	foreman start

dev:
	$(MANAGE) runserver --settings=giffeed.debug_settings

dumpdata:
	$(MANAGE) dumpdata auth.User bots core --indent 4 > bots.json

reset:
	python manage.py sqlclear core bots admin auth | python manage.py dbshell

syncdb:
	python manage.py syncdb

edit:
	DJANGO_SETTINGS_MODULE=giffeed.settings gvim .

test:
	$(MANAGE) test bots core


# Commands starting with h are the same only for Heroku

hsyncdb:
	$(HMANAGE) syncdb
