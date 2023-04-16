# Generated by Django 2.2.28 on 2023-04-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20230413_1607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'List of all admin panel user', 'verbose_name_plural': 'List of all admin panel users'},
        ),
        migrations.AddField(
            model_name='user',
            name='contact_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Contact Number'),
        ),
    ]