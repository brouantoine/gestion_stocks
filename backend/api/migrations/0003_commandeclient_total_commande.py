# Generated by Django 5.2.1 on 2025-05-31 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_emplacement_commandeclient_lignecommandeclient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandeclient',
            name='total_commande',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
