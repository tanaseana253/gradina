import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradinaCraciun.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test email',
    'Acesta este un test',
    settings.DEFAULT_FROM_EMAIL,
    ['tanase_ana253@yahoo.com'],
    fail_silently=False
)

print("Email trimis (sau a dat eroare)")