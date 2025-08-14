from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('users', 'User')
    username = "abdul"
    email = "abdulwahhabmuhyideen@gmail.com"
    password = "Abdul#12345"  

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
