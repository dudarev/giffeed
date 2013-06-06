Clone

```bash
git clone git@github.com:dudarev/giffeed.git
cd giffeed
```

Install requirements


```bash
mkvirtualenv giffeed
pip install -r requirements.txt
```

Set up PostgreSQL database. See section "Setting up db with postgres" at http://dudarev.com/wiki/Python.html.

Create file `giffeed/local_settings.py`:

```
import dj_database_url
from settings import SITE_ROOT
DATABASES = {'default': dj_database_url.config(default='postgres://USER:PASSWORD@localhost/DB_NAME')}

STATIC_URL = '/static/'
STATICFILES_DIRS = ( '%s/giffeed/static/' % (SITE_ROOT), )
```

```bash
make syncdb
make dev
```

Navigate to http://localhost:8000/
