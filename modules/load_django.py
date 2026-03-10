import sys
import os
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brain_com_ua')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brain_com_ua.settings")
django.setup()