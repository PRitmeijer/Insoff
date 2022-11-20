"""
WSGI config for insoff project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insoff.settings')
sys.path.append(os.path.join(settings.BASE_DIR, "apps"))

application = get_wsgi_application()
