# Generated by Django 3.2.5 on 2021-11-07 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0008_alter_complaint_details_currently_with'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint_details',
            name='Currently_with',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='myResidenceService.sec_incharge'),
        ),
    ]