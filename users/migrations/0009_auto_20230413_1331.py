# Generated by Django 2.2.28 on 2023-04-13 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_client_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('superadmin', 'Super Admin'), ('admin', 'Admin'), ('client', 'Client'), ('coach', 'Coach'), ('coachee', 'Coachee')], default='Super Admin', max_length=10),
        ),
    ]
