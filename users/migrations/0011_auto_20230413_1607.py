# Generated by Django 2.2.28 on 2023-04-13 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20230413_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('superadmin', 'Super Admin'), ('admin', 'Admin'), ('client', 'Client'), ('coach', 'Coach'), ('coachee', 'Coachee')], default='superadmin', max_length=30),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]
