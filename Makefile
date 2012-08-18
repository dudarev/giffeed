MANAGE= python manage.py
HMANAGE= heroku run python manage.py

syncdb:
	python manage.py syncdb

edit:
	DJANGO_SETTINGS_MODULE=giffeed.settings gvim .

migrate:
ifndef APP
	$(MANAGE) migrate
else
	@echo Starting of migration of $(APP)
	$(MANAGE) schemamigration $(APP) --auto
	$(MANAGE) migrate $(APP)
	@echo Done
endif

migrate_init:
ifndef APP
	@echo Please, specify -e APP=appname argument
else
	@echo Starting init migration of $(APP)
	$(MANAGE) schemamigration $(APP) --initial
	$(MANAGE) migrate $(APP)
	@echo Done
endif

test:
	$(MANAGE) test bots core


# Commands starting with h are the same only for Heroku

hsyncdb:
	$(HMANAGE) syncdb

hmigrate:
ifndef APP
	$(HMANAGE) migrate
else
	@echo Starting of migration of $(APP) on Heroku
	$(HMANAGE) migrate $(APP)
	@echo Done
endif
