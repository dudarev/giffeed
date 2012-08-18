syncdb:
	python manage.py syncdb

# Commands starting with h are the same only for Heroku

hsyncdb:
	heroku run python manage.py syncdb
