# Generated by Django 3.2.5 on 2021-10-24 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0016_auto_20211024_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaint_details',
            old_name='Qtr_ID',
            new_name='Qtr',
        ),
    ]