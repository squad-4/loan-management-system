import os

from project.settings.common import *

SECRET_KEY = "c*!n=-f2rcxe430=zkyp)=7he$l1e9mk^^u%qq+g**sd2^b90)"
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
