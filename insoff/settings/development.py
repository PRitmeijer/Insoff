from insoff.settings.production import *

TMP_PATH = os.path.abspath(os.path.join(BASE_DIR, 'tmp'))

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TMP_PATH, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.abspath(os.path.join(TMP_PATH, 'static_root'))