# Generated by Django 3.2.5 on 2021-12-11 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0011_alter_complaint_details_complaint_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint_details',
            name='Complaint_no',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]
