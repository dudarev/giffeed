MANAGE= python manage.py
HMANAGE= heroku run python manage.py

run:
	foreman start

dev:
	$(MANAGE) runserver --settings=giffeed.debug_settings

dumpdata:
	$(MANAGE) dumpdata auth.User bots --indent 4 > bots.json

syncdb:
	python manage.py syncdb

edit:
	DJANGO_SETTINGS_MODULE=giffeed.settings gvim .

test:
	$(MANAGE) test bots core


# Commands starting with h are the same only for Heroku

hsyncdb:
	$(HMANAGE) syncdb
