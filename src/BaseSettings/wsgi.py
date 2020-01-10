"""
WSGI config for BaseSettings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os , sys
from django.core.wsgi import get_wsgi_application
# add the hellodjango project path into the sys.path
# sys.path.append('/var/www/html/biobank/')

# add the virtualenv site-packages path to the sys.path
# sys.path.append('/var/www/html/biobank/myvenv/lib/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BaseSettings.settings")

application = get_wsgi_application()
