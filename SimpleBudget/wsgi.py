"""
WSGI config for SimpleBudget project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimpleBudget.settings")


if os.environ.get("RUN_MIGRATIONS") == "1":
    from SimpleBudget.startup import run
    run()

application = get_wsgi_application()


