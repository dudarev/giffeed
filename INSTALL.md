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

To run:

```bash
make syncdb
make dev
```

Navigate to http://localhost:8000/

To create a bot got got http://localhost:8000/admin/ and create a bot with

    name: -imgur
    URL: http://feeds.feedburner.com/ImgurGallery?format=xml
    
Minus sign in front of the name is important. Go to the main page again, refresh it, the bot should load latest GIFs from Imgur feed.
