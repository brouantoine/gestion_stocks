# Generated by Django 5.2.1 on 2025-06-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_module_allowed_roles_module_llowed_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='llowed_roles',
        ),
        migrations.AddField(
            model_name='module',
            name='allowed_roles',
            field=models.CharField(default='admin', max_length=200),
        ),
    ]
