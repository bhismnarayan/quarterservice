# Generated by Django 4.0.5 on 2022-07-04 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0002_alter_sse_colony_groupname'),
    ]

    operations = [
        migrations.AddField(
            model_name='sse_colony',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]