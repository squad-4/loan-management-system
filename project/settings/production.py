import os

import dj_database_url

from project.settings.common import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql_psycopg2"}}
DATABASES["default"].update(dj_database_url.config())
