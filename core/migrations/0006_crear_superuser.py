from django.db import migrations


def crear_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@foodplease.com',
            password='Admin12345'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_nombre_de_tu_ultima_migracion'),
    ]

    operations = [
        migrations.RunPython(crear_superuser),
    ]