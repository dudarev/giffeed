# pull in the normal settings
from settings import *
from local_settings import *

DEBUG = True

STATIC_URL = '/static/'
STATICFILES_DIRS = ('%s/giffeed/static/' % SITE_ROOT)
