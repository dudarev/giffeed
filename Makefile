syncdb:
	python manage.py syncdb

edit:
	DJANGO_SETTINGS_MODULE=giffeed.settings gvim .

# Commands starting with h are the same only for Heroku

hsyncdb:
	heroku run python manage.py syncdb
