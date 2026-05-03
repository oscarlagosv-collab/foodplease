from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import os

        if os.environ.get('CREATE_SUPERUSER') == '1':
            from django.contrib.auth.models import User

            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Oscar')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'oscarlagosv@gmail.com')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Oscar316')

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)