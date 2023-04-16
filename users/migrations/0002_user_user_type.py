# Generated by Django 2.2.28 on 2023-04-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('superuser', 'Superuser')], default='superuser', max_length=10),
        ),
    ]
